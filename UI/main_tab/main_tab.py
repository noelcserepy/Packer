import json
from PySide6.QtWidgets import *
from UI.main_tab.main_table import MainTable

settings = json.load(open("settings.json", "r"))


class MainTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()


    def setup(self):
        height = 800
        width = 1000
        main_table = MainTable()
        # main_table.setMinimumHeight(height)
        # main_table.setMaximumHeight(height)
        # main_table.setMinimumWidth(width)
        # main_table.setMaximumWidth(width)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
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
