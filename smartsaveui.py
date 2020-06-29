import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import mayautils


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class SmartSaveUI(QtWidgets.QDialog):
    """Simple UI Class"""

    def __init__(self):
        """Constructor"""
        # Passing the object SimpleUI as an argument to super()
        # makes this line python 2 and 3 compatible.
        super(SmartSaveUI, self).__init__(parent=maya_main_window())
        self.scene = mayautils.SceneFile()

        self.setWindowTitle("Smart Save")
        self.resize(500, 200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create widgets for our UI"""
        self.title_lbl = QtWidgets.QLabel('Smart Save')
        self.title_lbl.setStyleSheet('font: bold 40px')

        self.dir_lbl = QtWidgets.QLabel('Directory')
        self.dir_le = QtWidgets.QLineEdit()
        self.dir_le.setText(self.scene.dir)
        self.browse_btn = QtWidgets.QPushButton('Browse...')

        self.descriptor_lbl = QtWidgets.QLabel('Descriptor')
        self.descriptor_le = QtWidgets.QLineEdit()
        self.descriptor_le.setText(self.scene.descriptor)

        self.version_lbl = QtWidgets.QLabel('Version')
        self.version_spinbox = QtWidgets.QSpinBox()
        self.version_spinbox.setValue(self.scene.version)

        self.ext_lbl = QtWidgets.QLabel('Extension')
        self.ext_le = QtWidgets.QLineEdit('ma')
        self.ext_le.setText(self.scene.ext)

        self.save_btn = QtWidgets.QPushButton('Save')
        self.increment_save_btn = QtWidgets.QPushButton('Increment and Save')
        self.cancel_btn = QtWidgets.QPushButton('Cancel')

    def create_layout(self):
        """Lay out our widgets in the UI"""
        self.directory_layout = QtWidgets.QHBoxLayout()
        self.directory_layout.addWidget(self.dir_lbl)
        self.directory_layout.addWidget(self.dir_le)
        self.directory_layout.addWidget(self.browse_btn)

        self.descriptor_layout = QtWidgets.QHBoxLayout()
        self.descriptor_layout.addWidget(self.descriptor_lbl)
        self.descriptor_layout.addWidget(self.descriptor_le)

        self.version_layout = QtWidgets.QHBoxLayout()
        self.version_layout.addWidget(self.version_lbl)
        self.version_layout.addWidget(self.version_spinbox)

        self.ext_layout = QtWidgets.QHBoxLayout()
        self.ext_layout.addWidget(self.ext_lbl)
        self.ext_layout.addWidget(self.ext_le)

        self.bottom_btn_layout = QtWidgets.QHBoxLayout()
        self.bottom_btn_layout.addWidget(self.increment_save_btn)
        self.bottom_btn_layout.addWidget(self.save_btn)
        self.bottom_btn_layout.addWidget(self.cancel_btn)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.title_lbl)
        self.main_layout.addLayout(self.directory_layout)
        self.main_layout.addLayout(self.descriptor_layout)
        self.main_layout.addLayout(self.version_layout)
        self.main_layout.addLayout(self.ext_layout)

        self.main_layout.addStretch()

        self.main_layout.addLayout(self.bottom_btn_layout)
        self.setLayout(self.main_layout)

    def create_connections(self):
        """Connect our widgets signals to slots"""
        self.cancel_btn.clicked.connect(self.cancel)
        self.save_btn.clicked.connect(self.save)
        self.increment_save_btn.clicked.connect(self.increment_save)
        self.browse_btn.clicked.connect(self.browse)

    def _populate_scenefile_properties(self):
        """Populates the SceneFile object's properties from the UI"""
        self.scene.dir = self.dir_le.text()
        self.scene.descriptor = self.descriptor_le.text()
        self.scene.version = self.version_spinbox.value()
        self.scene.ext = self.ext_le.text()

    @QtCore.Slot()
    def save(self):
        """Save the scene file"""
        self._populate_scenefile_properties()
        self.scene.save()

    @QtCore.Slot()
    def increment_save(self):
        """Automatically finds the next available version on disk and saves up."""
        self._populate_scenefile_properties()
        self.scene.increment_and_save()

    @QtCore.Slot()
    def cancel(self):
        """Quits the dialog"""
        self.close()

    @QtCore.Slot()
    def browse(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        filename = dialog.getOpenFileName()[0]

        last_slash_index = filename.rfind('/')
        last_underscore_index = filename.rfind('_')
        last_dot_index = filename.rfind('.')

        self.scene.directory = filename[: last_slash_index + 1]
        self.scene.descriptor = filename[last_slash_index + 1 : last_underscore_index]
        self.scene.version = int(filename[last_underscore_index + 1 : last_dot_index])
        self.scene.ext = filename[last_dot_index + 1 :]

        self.dir_le.setText(self.scene.directory)
        self.descriptor_le.setText(self.scene.descriptor)
        self.version_spinbox.setValue(self.scene.version)
        self.ext_le.setText(self.scene.ext)

        cmds.file(filename, open=True)
