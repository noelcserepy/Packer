import sys
from UI.settings_tab import SettingsTab
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

        self.addTab(MainTab(), "Main")
        self.addTab(SettingsTab(), "Settings")


class MainTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        main()
        self.button = QPushButton("Click me!")
        self.text = QLabel("main", alignment=QtCore.Qt.AlignLeft)
        self.text2 = QLabel("Do stuff", alignment=QtCore.Qt.AlignLeft)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.text2)


if __name__ == "__main__":
    app = QApplication([])

    widget = MainWindow()
    apply_stylesheet(app, theme='dark_cyan.xml')
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec())


