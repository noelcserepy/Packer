import sys
from tex_import import get_groups
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("TexImport")
        self.setGeometry(100, 100, 50, 150)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(Tabs())
    

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
        self.button = QPushButton("Click me!")
        self.text = QLabel("main",
                            alignment=QtCore.Qt.AlignLeft)
        self.text2 = QLabel("Do stuff",
                            alignment=QtCore.Qt.AlignLeft)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.text2)


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()


    def setup(self):
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(DirSelect())
        self.layout.addWidget(PackingGroupAdd())
        self.layout.addWidget(ExtensionSelect())
        self.layout.addWidget(IdentifierSelect())


class IdentifierSelect(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        pass


class ExtensionSelect(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        pass


class PackingGroupAdd(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTitle("Packing Groups")

        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")
        
        self.layout = QVBoxLayout(self)
        
        self.layout.addWidget(PackingGroupSelect())
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.remove_button)



class PackingGroupSelect(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.textures = ["Roughness", "Metallic", "Ambient Occlusion", "Curvature", "ID"]
        self.textures.insert(0, "Empty")

        self.identifier = QLineEdit()
        self.identifier.setPlaceholderText("Identifier")

        self.texture_r = QComboBox()
        self.texture_r.setPlaceholderText("Red Channel")
        self.texture_r.insertItems(0, self.textures)

        self.texture_g = QComboBox()
        self.texture_g.setPlaceholderText("Green Channel")
        self.texture_g.insertItems(0, self.textures)

        self.texture_b = QComboBox()
        self.texture_b.setPlaceholderText("Blue Channel")
        self.texture_b.insertItems(0, self.textures)

        self.texture_a = QComboBox()
        self.texture_a.setPlaceholderText("Alpha Channel")
        self.texture_a.insertItems(0, self.textures)

        self.packing_groups_list = QPushButton("gaggi")

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.identifier)
        self.layout.addWidget(self.texture_r)
        self.layout.addWidget(self.texture_g)
        self.layout.addWidget(self.texture_b)
        self.layout.addWidget(self.texture_a)


class DirSelect(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTitle("Asset Directory")
        self.directory_edit = QLineEdit()
        self.selectbutton = QPushButton("Select")
        self.selectbutton.clicked.connect(self.open_file_dialog)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.directory_edit)
        self.layout.addWidget(self.selectbutton)
        

    @QtCore.Slot()
    def open_file_dialog(self):
        dir_dialog = FileDialog()
        dir_dialog.exec()
        selected_dir = dir_dialog.selectedFiles()[0]
        self.directory_edit.setText(selected_dir)


class FileDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.fileMode
        self.setFileMode(self.Directory)
        self.setDirectory("C:\\")
        self.setViewMode(self.List)
        self.setOption(self.ShowDirsOnly, on=True)



if __name__ == "__main__":
    app = QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())



