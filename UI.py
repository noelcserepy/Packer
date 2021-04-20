import sys
import json
from tex_import import get_groups
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *

@QtCore.Slot()
def printhi():
    print("hi")


settings = json.load(open("settings.json", "r"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("TexImport")
        self.setGeometry(100, 100, 100, 300)
        self.setCentralWidget(Tabs())


class SaveSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.on_save_clicked)
        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.on_reset_clicked)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.save_button)
        
    def on_save_clicked(self):
        try:
            user_settings = json.load(open("user_settings.json", "r"))
        except:
            print("No settings here.")
            return

        with open("settings.json", "w") as f:
            json.dump(user_settings, f)

    def on_reset_clicked(self):
        try:
            default_settings = json.load(open("settings_default.json", "r"))
        except:
            print("No default settings here.")
            return

        with open("settings.json", "w") as f:
            json.dump(default_settings, f)


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
        self.dirselect  = DirSelect()
        self.identifierselect  = IdentifierSelect()
        self.extensionselect  = ExtensionSelect()
        self.packinggroupselect  = PackingGroupSelect()
        self.save = QWidget(self)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(printhi())
        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.on_reset_clicked)

        self.save.layout = QHBoxLayout(self.save)
        self.save.layout.addWidget(self.reset_button)
        self.save.layout.addWidget(self.save_button)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.dirselect, 0, 0, 1, 2)
        self.layout.addWidget(self.identifierselect, 1, 0, 1, 1)
        self.layout.addWidget(self.extensionselect, 1, 1, 1, 1)
        self.layout.addWidget(self.packinggroupselect, 2, 0, 1, 2)
        self.layout.addWidget(self.save, 3, 1, 1, 1)
        
    def on_save_clicked(self):
        try:
            print(self.dirselect.tw)
            user_settings = json.load(open("user_settings.json", "r"))
        except:
            print("No settings here.")
            return

        with open("settings.json", "w") as f:
            json.dump(user_settings, f)

    def on_reset_clicked(self):
        try:
            default_settings = json.load(open("settings_default.json", "r"))
        except:
            print("No default settings here.")
            return

        with open("settings.json", "w") as f:
            json.dump(default_settings, f)
        

class IdentifierSelect(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTitle("Identifier Select")
        self.description = ("Select what texture identifiers to look for "
                            "e.g. \"R_\" in R_assetName.png or \"_r\" in assetName_r.png")
        self.identifier_data = settings["default_replacements"]
        self.description_text = QLabel(self.description,
                                        alignment=QtCore.Qt.AlignLeft)

        self.tw = QTreeWidget()
        self.tw.setAlternatingRowColors(True)
        self.tw.setHeaderLabels([
            "Identifier", 
            "Position"])
        for id in self.identifier_data:
            data = [id[0], id[-1]]
            QTreeWidgetItem(self.tw, data)

        self.id_select = QWidget()

        self.identifier = QLineEdit(self.id_select)
        self.identifier.setPlaceholderText("Identifier")

        self.position = QComboBox(self.id_select)
        self.position.setPlaceholderText("Position")
        self.position.insertItems(0, ["Start", "End"])

        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.on_add_clicked)
        self.remove_button = QPushButton("-")
        self.remove_button.clicked.connect(self.on_remove_clicked)

        self.id_select.layout = QHBoxLayout(self.id_select)
        self.id_select.layout.addWidget(self.identifier)
        self.id_select.layout.addWidget(self.position)
        self.id_select.layout.addWidget(self.add_button)
        self.id_select.layout.addWidget(self.remove_button)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.description_text)
        self.layout.addWidget(self.tw)
        self.layout.addWidget(self.id_select)
        

    def on_add_clicked(self):
        id = self.identifier.text()
        pos = self.position.currentText()
        QTreeWidgetItem(self.tw, [id, pos])

    def on_remove_clicked(self):
        current = self.tw.currentItem()
        index = self.tw.indexOfTopLevelItem(current)
        self.tw.takeTopLevelItem(index)


class ExtensionSelect(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTitle("Extension Select")
        self.description = ("Select what extensions to look for "
                            "e.g. PNG, JPG, TGA. "
                            "This is not case sensitive.")
        self.extensions_data = settings["extensions"]
        self.description_text = QLabel(self.description,
                                        alignment=QtCore.Qt.AlignLeft)

        self.lw = QListWidget()
        self.lw.setAlternatingRowColors(True)
        self.lw.addItems(self.extensions_data)

        self.ex_select = QWidget()

        self.extension = QLineEdit(self.ex_select)
        self.extension.setPlaceholderText("Extension")

        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.on_add_clicked)
        self.remove_button = QPushButton("-")
        self.remove_button.clicked.connect(self.on_remove_clicked)

        self.ex_select.layout = QHBoxLayout(self.ex_select)
        self.ex_select.layout.addWidget(self.extension)
        self.ex_select.layout.addWidget(self.add_button)
        self.ex_select.layout.addWidget(self.remove_button)        

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.description_text)
        self.layout.addWidget(self.lw)
        self.layout.addWidget(self.ex_select)

    def on_add_clicked(self):
        ex = self.extension.text()
        self.lw.addItem(ex)

    def on_remove_clicked(self):
        current = self.lw.currentRow()
        self.lw.takeItem(current)


class PackingGroupSelect(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTitle("Packing Groups")
        self.description = ("Packing groups define which texture maps should be packed into one file. "
                            "You may choose which channels these textures will populate. "
                            "The identifier signifies what letters to use to identify this new file "
                            "e.g. \"Identifier_AssetName.PNG\".")
        self.packing_groups_data = settings["packing_groups"]
        self.channels = ["Red Channel", "Green Channel", "Blue Channel", "Alpha Channel"]
        self.textures = settings["textures"]
        self.textures.insert(0, "Empty")
        self.fields = []

        self.description_text = QLabel(self.description,
                                        alignment=QtCore.Qt.AlignLeft)

        self.tw = QTreeWidget()
        self.tw.setAlternatingRowColors(True)
        self.tw.setHeaderLabels([
            "Identifier", 
            "Extension",
            "Red Channel", 
            "Green Channel", 
            "Blue Channel", 
            "Alpha Channel"
        ])

        for group in self.packing_groups_data:
            data = [group["identifier"]] + [group["extension"]] + group["group"]
            item = QTreeWidgetItem(self.tw, data)

        self.pg_select = QWidget()
        identifier = QLineEdit(self.pg_select)
        identifier.setPlaceholderText("Identifier")
        self.fields.append(identifier)

        extension = QLineEdit(self.pg_select)
        extension.setPlaceholderText("Extension")
        self.fields.append(extension)

        for channel in self.channels:
            item = QComboBox(self.pg_select)
            item.setPlaceholderText(channel)
            item.insertItems(0, self.textures)
            self.fields.append(item)

        self.pg_select.layout = QHBoxLayout(self.pg_select)
        for field in self.fields:
            self.pg_select.layout.addWidget(field)

        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.on_add_clicked)
        self.remove_button = QPushButton("-")
        self.remove_button.clicked.connect(self.on_remove_clicked)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.description_text, 0, 0, 1, 2)
        self.layout.addWidget(self.tw, 1, 0, 2, -1)
        self.layout.addWidget(self.pg_select, 4, 0, 1, 3)
        self.layout.addWidget(self.add_button, 4, 4, 1, 1)
        self.layout.addWidget(self.remove_button, 4, 5, 1, 1)

    def on_add_clicked(self):
        i = self.fields[0].text()
        e = self.fields[1].text()
        r = self.fields[2].currentText()
        g = self.fields[3].currentText()
        b = self.fields[4].currentText()
        a = self.fields[5].currentText()
        QTreeWidgetItem(self.tw, [i, e, r, g, b, a])
    
    def on_remove_clicked(self):
        current = self.tw.currentItem()
        index = self.tw.indexOfTopLevelItem(current)
        self.tw.takeTopLevelItem(index)


class DirSelect(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTitle("Asset Directory")
        self.description = ("Select the directory that will be searched for textures. "
                            "Subdirectories will also be searched")
        self.description_text = QLabel(self.description,
                                        alignment=QtCore.Qt.AlignLeft)
        self.directory_edit = QLineEdit()
        self.selectbutton = QPushButton("Select")
        self.selectbutton.clicked.connect(self.open_file_dialog)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.description_text, 0, 0, 1, 1)
        self.layout.addWidget(self.directory_edit, 1, 0, 1, 1)
        self.layout.addWidget(self.selectbutton, 1, 2, 1, 1)
        

    @QtCore.Slot()
    def open_file_dialog(self):
        fd = QFileDialog()
        fd.setFileMode(fd.Directory)
        fd.setDirectory("C:\\")
        fd.setViewMode(fd.List)
        fd.setOption(fd.ShowDirsOnly, on=True)

        fd.exec()
        selected_dir = fd.selectedFiles()[0]
        self.directory_edit.setText(selected_dir)



if __name__ == "__main__":
    app = QApplication([])

    widget = MainWindow()
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec_())



