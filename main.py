import sys
from PySide6.QtWidgets import QMainWindow, QTabWidget, QApplication
from UI.settings_tab.settings_tab import SettingsTab
from UI.main_tab.main_tab import MainTab
from packer.packer import Packer


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
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
        self.setTabPosition(QTabWidget.West)

        Packer().scan()
        self.addTab(MainTab(), "Main")
        self.addTab(SettingsTab(), "Settings")


if __name__ == "__main__":
    app = QApplication([])
    win = MainWindow(app)
    style = "UI/style.css"
    win.show()
    sys.exit(app.exec_())
