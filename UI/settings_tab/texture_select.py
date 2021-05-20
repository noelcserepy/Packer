from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *
from UI.settings_tab.texture_dialog import TextureEditDialog

class TextureSelect(QGroupBox):
    def __init__(self, settings):
        super().__init__()
        self.header_font=QtGui.QFont()
        self.header_font.setBold(True)
        self.setup(settings)

    def setup(self, settings):
        self.setTitle("Texture Info")
        self.description = ("Define what input textures TexImport should look for.")
        self.description_text = QLabel(self.description, alignment=QtCore.Qt.AlignLeft)

        self.tex_info_widget = QWidget()

        # Displays list of saved textures.
        self.tex_list = QListWidget()
        self.tex_list.setAlternatingRowColors(False)
        for tex in settings["textures"]:
            tex_item = QListWidgetItem()
            tex_item.setData(QtCore.Qt.UserRole, tex)
            tex_item.setText(tex["name"])
            self.tex_list.addItem(tex_item)
        self.tex_list.setCurrentRow(0)
        self.tex_list.itemSelectionChanged.connect(self.on_current_changed)

        # Sets up fields for displaying texture information.
        self.tex_info_box = QWidget()
        self.tex_info_box_labels = QWidget()

        self.name_header = QLabel("Name:", alignment=QtCore.Qt.AlignLeft)
        self.name_header.setFont(self.header_font)
        self.name = QLabel("", alignment=QtCore.Qt.AlignLeft)

        self.preferred_header = QLabel("Preferred Identifier:", alignment=QtCore.Qt.AlignLeft)
        self.preferred_header.setFont(self.header_font)
        self.preferred = QLabel("", alignment=QtCore.Qt.AlignLeft)

        self.tex_info_box_labels.layout = QHBoxLayout(self.tex_info_box_labels)
        self.tex_info_box_labels.layout.addWidget(self.name_header)
        self.tex_info_box_labels.layout.addWidget(self.name)
        self.tex_info_box_labels.layout.addWidget(self.preferred_header)
        self.tex_info_box_labels.layout.addWidget(self.preferred)

        self.identifiers_header = QLabel("Identifiers:", alignment=QtCore.Qt.AlignLeft)
        self.identifiers_header.setFont(self.header_font)
        self.identifiers = QListWidget()
        self.identifiers.setMinimumHeight(50)
        
        self.extensions_header = QLabel("Extensions:", alignment=QtCore.Qt.AlignLeft)
        self.extensions_header.setFont(self.header_font)
        self.extensions = QListWidget()
        self.extensions.setMinimumHeight(50)

        self.on_current_changed()

        

        self.tex_info_box.layout = QVBoxLayout(self.tex_info_box)
        self.tex_info_box.layout.addWidget(self.tex_info_box_labels)
        self.tex_info_box.layout.addWidget(self.identifiers_header)
        self.tex_info_box.layout.addWidget(self.identifiers)
        self.tex_info_box.layout.addWidget(self.extensions_header)
        self.tex_info_box.layout.addWidget(self.extensions)

        self.tex_info_widget.layout = QHBoxLayout(self.tex_info_widget)
        self.tex_info_widget.layout.addWidget(self.tex_list)
        self.tex_info_widget.layout.addWidget(self.tex_info_box)

        self.tex_button_widget = QWidget()
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.on_add_clicked)
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.on_edit_clicked)
        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.on_remove_clicked)

        self.tex_button_widget.layout = QHBoxLayout(self.tex_button_widget)
        self.tex_button_widget.layout.addWidget(self.add_button)
        self.tex_button_widget.layout.addWidget(self.edit_button)
        self.tex_button_widget.layout.addWidget(self.remove_button)
    
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.description_text)
        self.layout.addWidget(self.tex_info_widget)
        self.layout.addWidget(self.tex_button_widget)
        
        
    def on_add_clicked(self):
        ted = TextureEditDialog(self, edit_index=-1)
        ted.setModal(True)
        ted.submitted.connect(self.add_new_item)
        ted.exec()

    def on_edit_clicked(self):
        selected_row = self.tex_list.currentRow()
        selected_data = self.tex_list.currentItem().data(QtCore.Qt.UserRole)
        ted = TextureEditDialog(self, edit_index=selected_row, data=selected_data)
        ted.setModal(True)
        ted.submitted.connect(self.add_new_item)
        ted.exec()

    @QtCore.Slot(dict, QListWidgetItem)
    def add_new_item(self, tex, edit_index):
        print(f"RECEIVED FROM SIGNAL: {tex}")
        tex_item = QListWidgetItem()
        tex_item.setData(QtCore.Qt.UserRole, tex)
        tex_item.setText(tex["name"])
        if edit_index > -1:
            self.tex_list.takeItem(edit_index)
            self.tex_list.insertItem(edit_index, tex_item)
            return
        self.tex_list.addItem(tex_item)
    
    def on_remove_clicked(self):
        current_row = self.tex_list.currentRow()
        self.tex_list.takeItem(current_row)

    def on_current_changed(self):
        self.selected = self.tex_list.currentItem().data(QtCore.Qt.UserRole)
        self.selected_name = self.selected["name"]
        self.selected_preferred = (self.selected["preferred_identifier"][0] + " " + 
                                    self.selected["preferred_identifier"][1])
        self.selected_identifiers = [str(i) for i in self.selected["identifiers"]]
        self.selected_extensions = self.selected["extensions"]

        self.name.setText(self.selected_name)
        self.preferred.setText(self.selected_preferred)
        self.identifiers.clear()
        self.identifiers.addItems(self.selected_identifiers)
        self.extensions.clear()
        self.extensions.addItems(self.selected_extensions)

    def get_data(self):
        data = []
        row_count = self.tex_list.count()
        for i in range(row_count):
            item = self.tex_list.item(i)
            item_data = item.data(QtCore.Qt.UserRole)
            data.append(item_data)
        return data
