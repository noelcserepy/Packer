from PySide6 import QtCore
from PySide6.QtWidgets import *



class TextureEditDialog(QDialog):
    submitted = QtCore.Signal(dict, int)

    def __init__(self, parent, edit_index=-1, data=None):
        super().__init__(parent=parent)
        self.data = data
        self.edit_index = edit_index
        self.setup()
        
    def setup(self):
        self.setModal(True)

        # Sets up fields for editing texture information
        self.tex_info_box = QWidget()

        self.name_header = QLabel("Name", alignment=QtCore.Qt.AlignLeft)
        self.name = QLineEdit("")
        self.name.setPlaceholderText("e.g. Color")

        self.preferred = PreferredSelect()
        self.identifiers = IdentifierSelect()
        self.extensions = ExtensionSelect()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.on_save_clicked)
        self.discard_button = QPushButton("Discard")
        self.discard_button.clicked.connect(self.on_discard_clicked)

        # Populates fields if data is passed
        if self.data:
            self.name.setText(self.data["name"])

            self.preferred.identifier.setText(self.data["preferred_identifier"][0])
            pos_index = 0 if self.data["preferred_identifier"][1] == "start" else 1
            self.preferred.position.setCurrentIndex(pos_index)

            for id in self.data["identifiers"]:
                item = QListWidgetItem()
                item.setText(str(id))
                item.setData(QtCore.Qt.UserRole, id)
                self.identifiers.id_list.addItem(item)

            self.extensions.ex_list.addItems(self.data["extensions"])

        self.buttons = QWidget()
        self.buttons.layout = QHBoxLayout(self.buttons)
        self.buttons.layout.addWidget(self.save_button)
        self.buttons.layout.addWidget(self.discard_button)

        self.tex_info_box.layout = QVBoxLayout(self.tex_info_box)
        self.tex_info_box.layout.addWidget(self.name_header)
        self.tex_info_box.layout.addWidget(self.name)
        self.tex_info_box.layout.addWidget(self.preferred)
        self.tex_info_box.layout.addWidget(self.identifiers)
        self.tex_info_box.layout.addWidget(self.extensions)
        self.tex_info_box.layout.addWidget(self.buttons)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.tex_info_box)

    def on_save_clicked(self):
        tex = {
            "name": self.name.text(),
            "preferred_identifier": self.preferred.export_items(),
            "identifiers": self.identifiers.export_items(),
            "extensions": self.extensions.export_items()
        }
        self.submitted.emit(tex, self.edit_index)
        self.close()

    def on_discard_clicked(self):
        self.close()


class PreferredSelect(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTitle("Preferred Identifier")
        self.description = ("Select what you would like this texture to be identified with "
                            "e.g. \"R_\" in R_assetName.png")
        self.description_text = QLabel(self.description, alignment=QtCore.Qt.AlignLeft)

        self.id_select = QWidget()
        self.identifier = QLineEdit(self.id_select)
        self.identifier.setPlaceholderText("Identifier")

        self.position = QComboBox(self.id_select)
        self.position.setPlaceholderText("Position")
        self.position.insertItems(0, ["start", "end"])

        self.id_select.layout = QHBoxLayout(self.id_select)
        self.id_select.layout.addWidget(self.identifier)
        self.id_select.layout.addWidget(self.position)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.description_text)
        self.layout.addWidget(self.id_select)

    def export_items(self):
        id = self.identifier.text()
        pos = self.position.currentText()
        pref = [id, pos]
        return pref


class IdentifierSelect(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTitle("Identifier Select")
        self.description = ("Select what texture identifiers to look for "
                            "e.g. \"R_\" in R_assetName.png or \"_r\" in assetName_r.png")
        self.description_text = QLabel(self.description, alignment=QtCore.Qt.AlignLeft)

        self.id_list = QListWidget()
        self.id_select = QWidget()
        self.identifier = QLineEdit(self.id_select)
        self.identifier.setPlaceholderText("Identifier")

        self.position = QComboBox(self.id_select)
        self.position.setPlaceholderText("Position")
        self.position.insertItems(0, ["start", "end"])

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
        self.layout.addWidget(self.id_list)
        self.layout.addWidget(self.id_select)
        
    def on_add_clicked(self):
        id = self.identifier.text()
        pos = self.position.currentText()
        if not (id and pos):
            return
        item = QListWidgetItem()
        item.setText(f"['{id}', '{pos}']")
        item.setData(QtCore.Qt.UserRole, [id, pos])
        self.id_list.addItem(item)

    def on_remove_clicked(self):
        currentrow = self.id_list.currentRow()
        self.id_list.takeItem(currentrow)

    def export_items(self):
        row_count = self.id_list.count()
        all_identifiers = []
        for i in range(row_count):
            item = self.id_list.item(i)
            all_identifiers.append(item.data(QtCore.Qt.UserRole))
        return all_identifiers
            

class ExtensionSelect(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTitle("Extension Select")
        self.description = ("Select what extensions to look for "
                            "e.g. PNG, JPG, TGA. "
                            "This is not case sensitive.")
        self.description_text = QLabel(self.description, alignment=QtCore.Qt.AlignLeft)

        self.ex_list = QListWidget()
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
        self.layout.addWidget(self.ex_list)
        self.layout.addWidget(self.ex_select)
        
    def on_add_clicked(self):
        id = self.extension.text()
        if not id:
            return
        self.ex_list.addItem(id)

    def on_remove_clicked(self):
        currentrow = self.ex_list.currentRow()
        self.ex_list.takeItem(currentrow)

    def export_items(self):
        row_count = self.ex_list.count()
        all_extensions = []
        for i in range(row_count):
            item = self.ex_list.item(i)
            all_extensions.append(item.text())
        return all_extensions
