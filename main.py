import sys
import os
from UI.settings_tab.settings_tab import SettingsTab
from UI.main_tab.main_tab import MainTab
from packer.packer import Packer
from PySide6.QtWidgets import *
from qt_material import apply_stylesheet



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("Packer")
        self.resize(1080, 566)
        self.setCentralWidget(Tabs())


class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setMovable(False)
        self.setTabsClosable(False)

        Packer()
        self.addTab(MainTab(), "Main")
        self.addTab(SettingsTab(), "Settings")


if __name__ == "__main__":
    app = QApplication([])
    win = MainWindow()
    apply_stylesheet(app, theme='dark_cyan.xml')
    win.show()
    sys.exit(app.exec_())



