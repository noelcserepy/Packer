from PySide6 import QtCore
from PySide6.QtWidgets import *



class TextureEditDialog(QDialog):
    def __init__(self, parent, data_signal, data=None):
        super().__init__(parent=parent)
        self.data = data
        self.data_gathered = data_signal
        self.setup()
        
    def setup(self):
        self.setModal(True)

        # Sets up fields for editing texture information
        self.tex_info_box = QWidget()

        self.name_header = QLabel("Name", alignment=QtCore.Qt.AlignLeft)
        self.name = QLineEdit("")
        self.name.setPlaceholderText("e.g. Color")

        self.preferred_header = QLabel("Preferred Identifier", alignment=QtCore.Qt.AlignLeft)
        self.preferred = QLineEdit("")
        self.preferred.setPlaceholderText("e.g. D_, start")

        self.identifiers = IdentifierSelect()
        self.extensions = ExtensionSelect()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.on_save_clicked)
        self.discard_button = QPushButton("Discard")
        self.discard_button.clicked.connect(self.on_discard_clicked)

        # Populates fields if data is passed
        if self.data:
            self.name.setText(self.data["name"])
            self.preferred.setText(str(self.data["preferred_identifier"]))
            ids = [str(id) for id in self.data["identifiers"]]
            self.identifiers.id_list.addItems(ids)
            self.extensions.ex_list.addItems(self.data["extensions"])

        self.buttons = QWidget()
        self.buttons.layout = QHBoxLayout(self.buttons)
        self.buttons.layout.addWidget(self.save_button)
        self.buttons.layout.addWidget(self.discard_button)

        self.tex_info_box.layout = QVBoxLayout(self.tex_info_box)
        self.tex_info_box.layout.addWidget(self.name_header)
        self.tex_info_box.layout.addWidget(self.name)
        self.tex_info_box.layout.addWidget(self.preferred_header)
        self.tex_info_box.layout.addWidget(self.preferred)
        self.tex_info_box.layout.addWidget(self.identifiers)
        self.tex_info_box.layout.addWidget(self.extensions)
        self.tex_info_box.layout.addWidget(self.buttons)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.tex_info_box)

    def on_save_clicked(self):
        tex = {
            "name": self.name,
            "preferred_identifier": self.preferred,
            "identifiers": self.identifiers.export_items(),
            "extensions": self.extensions.export_items()
        }
        print(tex)
        tex_item = QListWidgetItem()
        tex_item.setData(QtCore.Qt.UserRole, tex)
        tex_item.setText(tex["name"])
        self.data_gathered.emit(tex_item)
        self.tex_list.addItem(tex_item)

        self.close()

    def on_discard_clicked(self):
        self.close()


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
        self.layout.addWidget(self.id_list)
        self.layout.addWidget(self.id_select)
        
    def on_add_clicked(self):
        id = self.identifier.text()
        pos = self.position.currentText()
        if not (id and pos):
            return
        item = QListWidgetItem()
        item.setText(f"[{id}, {pos}]")
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
            all_identifiers.append(item.data())
            

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