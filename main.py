import sys
from UI.settings_tab.settings_tab import SettingsTab
from UI.main_tab.main_tab import MainTab
from tex_import.tex_import import main
from PySide6 import QtCore
from PySide6.QtWidgets import *
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("TexImport")
        self.setGeometry(100, 100, 100, 300)
        self.setCentralWidget(Tabs())


class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTabShape(self.Rounded)
        self.setMovable(False)
        self.setTabsClosable(False)

        main()
        self.addTab(MainTab(), "Main")
        self.addTab(SettingsTab(), "Settings")


if __name__ == "__main__":
    app = QApplication([])

    widget = MainWindow()
    apply_stylesheet(app, theme='dark_cyan.xml')
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec())



