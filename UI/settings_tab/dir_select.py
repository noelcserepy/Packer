from PySide6 import QtCore
from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QFileDialog,
)


class DirSelect(QGroupBox):
    def __init__(self, settings):
        super().__init__()
        self.setup(settings)

    def setup(self, settings):
        self.setTitle("Asset Directory")
        self.description = (
            "Select the directory that will be searched for textures. "
            "Subdirectories will also be searched"
        )
        self.description_text = QLabel(self.description, alignment=QtCore.Qt.AlignLeft)
        self.directory_edit = QLineEdit()
        self.settings_dir = settings["search_directory"]
        self.directory_edit.setText(self.settings_dir)

        self.selectbutton = QPushButton("Select")
        self.selectbutton.clicked.connect(self.open_file_dialog)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.description_text, 0, 0, 1, 1)
        self.layout.addWidget(self.directory_edit, 1, 0, 1, 1)
        self.layout.addWidget(self.selectbutton, 1, 2, 1, 1)

    def open_file_dialog(self):
        fd = QFileDialog()
        fd.setFileMode(fd.Directory)
        fd.setDirectory("C:\\")
        fd.setViewMode(fd.List)
        fd.setOption(fd.ShowDirsOnly, on=True)

        fd.exec()
        selected_dir = fd.selectedFiles()[0]
        self.directory_edit.setText(selected_dir)

    def get_data(self):
        data = self.directory_edit.text()
        s_data = data.replace("\\", "/")
        return s_data
