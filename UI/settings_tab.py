import json
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *
from UI.texture_select import TextureSelect
from tex_import.tex_import import change_slashes



settings = json.load(open("settings.json", "r"))
with open("settings_tmp.json", "w") as f:
    json.dump(settings, f)


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.dirselect  = DirSelect()
        self.dirselect.setMinimumHeight(100)
        self.texture_select = TextureSelect(settings)
        self.texture_select.setMinimumHeight(400)
        self.texture_select.setMaximumWidth(600)
        self.packinggroupselect  = PackingGroupSelect()
        self.packinggroupselect.setMinimumHeight(300)
        self.packinggroupselect.setMaximumWidth(600)
        self.save = QWidget(self)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.print_data)
        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.on_reset_clicked)

        self.save.layout = QHBoxLayout(self.save)
        self.save.layout.addWidget(self.reset_button)
        self.save.layout.addWidget(self.save_button)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.dirselect, 0, 0, 1, 2)
        self.layout.addWidget(self.texture_select, 1, 0, 1, 2)
        self.layout.addWidget(self.packinggroupselect, 2, 0, 1, 2)
        self.layout.addWidget(self.save, 3, 1, 1, 1)
        
    def print_data(self):
        print(self.dirselect.get_data())
        print(self.identifierselect.get_data())
        print(self.extensionselect.get_data())
        print(self.packinggroupselect.get_data())

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
        

class DirSelect(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTitle("Asset Directory")
        self.description = ("Select the directory that will be searched for textures. "
                            "Subdirectories will also be searched")
        self.description_text = QLabel(self.description, alignment=QtCore.Qt.AlignLeft)
        self.directory_edit = QLineEdit()
        self.settings_dir = settings["sync_asset_dir"]
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
        self.textures = [tex["name"] for tex in settings["textures"]]
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

    def get_data(self):
        data = []
        for i in range(self.tw.topLevelItemCount()):
            item = self.tw.topLevelItem(i)
            item_data = {
                "identifier": item.text(0),
                "extension": item.text(1),
                "group": [
                    item.text(2), 
                    item.text(3),
                    item.text(4),
                    item.text(5)
                ]
            }
            data.append(item_data)

        return data


