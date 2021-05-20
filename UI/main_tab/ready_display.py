import json
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *



class ReadyDisplay(QGroupBox):
    def __init__(self, settings):
        super().__init__()
        self.header_font=QtGui.QFont()
        self.header_font.setBold(True)
        self.setup(settings)


    def setup(self, settings):
        self.setTitle("Assets Ready to Pack")
        self.description = ("Theses assets are ready to pack.")
        self.description_text = QLabel(self.description, alignment=QtCore.Qt.AlignLeft)

        self.tex_info_widget = QWidget()

        # Displays list of assets ready to pack.
        self.ready_groups = QListWidget()
        self.ready_groups.setAlternatingRowColors(False)
        self.layout = QVBoxLayout(self)
        pgroups = json.load(open("pgroups.json"))

        for group in pgroups:
            checkbox = QListWidgetItem()
            checkbox.setCheckState(QtCore.Qt.CheckState.Checked)
            data = (group["textures"][0]["asset_name"], group["group"]["identifier"])
            checkbox.setData(QtCore.Qt.UserRole, data)
            checkbox.setText(f"{data[0]} -> {data[1]}")
            self.ready_groups.addItem(checkbox)

        # Button widget to hold "Refresh" & "Pack" buttons
        self.button_widget = QWidget()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.on_refresh_clicked)
        self.pack_button = QPushButton("Pack")
        self.pack_button.clicked.connect(self.on_pack_clicked)

        self.button_widget.layout = QHBoxLayout(self.button_widget)
        self.button_widget.layout.addWidget(self.refresh_button)
        self.button_widget.layout.addWidget(self.pack_button)

        self.ready_groups.setCurrentRow(0)
        #self.layout.addWidget(self.description_text)
        self.layout.addWidget(self.ready_groups)
        self.layout.addWidget(self.button_widget)


    def on_refresh_clicked(self):
        pass
    #     ted = TextureEditDialog(self, edit_index=-1)
    #     ted.setModal(True)
    #     ted.submitted.connect(self.add_new_item)
    #     ted.exec()

    def on_pack_clicked(self):
        pass
    #     selected_row = self.tex_list.currentRow()
    #     selected_data = self.tex_list.currentItem().data(QtCore.Qt.UserRole)
    #     ted = TextureEditDialog(self, edit_index=selected_row, data=selected_data)
    #     ted.setModal(True)
    #     ted.submitted.connect(self.add_new_item)
    #     ted.exec()



    def get_data(self):
        data = []
        row_count = self.ready_groups.count()
        for i in range(row_count):
            item = self.ready_groups.item(i)
            item_data = item.data(QtCore.Qt.UserRole)
            data.append(item_data)
        return data
