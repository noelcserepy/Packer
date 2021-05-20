import json
from PySide6 import QtCore
from PySide6.QtWidgets import *
from UI.main_tab.ready_display import ReadyDisplay
from UI.main_tab.packed_display import PackedDisplay



settings = json.load(open("settings.json", "r"))


class MainTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()


    def setup(self):
        height = 800
        width = 300
        self.readydisplay = ReadyDisplay(settings)
        self.readydisplay.setMinimumHeight(height)
        self.readydisplay.setMaximumHeight(height)
        self.readydisplay.setMinimumWidth(width)
        self.readydisplay.setMaximumWidth(width)

        self.packeddisplay = PackedDisplay(settings)
        self.packeddisplay.setMinimumHeight(height)
        self.packeddisplay.setMaximumHeight(height)
        self.packeddisplay.setMinimumWidth(width)
        self.packeddisplay.setMaximumWidth(width)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.readydisplay)
        self.layout.addWidget(self.packeddisplay)


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