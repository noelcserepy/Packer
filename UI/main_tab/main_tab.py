import json
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFileDialog
)
from UI.main_tab.main_table import MainTable
from UI.main_tab.main_buttons import MainButtons

with open("settings.json", "r") as f:
    settings = json.load(f)


class MainTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()


    def setup(self):
        main_buttons = MainButtons()
        main_table = MainTable()

        layout = QVBoxLayout(self)
        layout.addWidget(main_buttons)
        layout.addWidget(main_table)
        

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
