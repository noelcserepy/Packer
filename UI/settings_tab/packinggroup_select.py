from PySide6 import QtCore
from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QLineEdit,
    QComboBox,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
)


class PackingGroupSelect(QGroupBox):
    def __init__(self, settings):
        super().__init__()
        self.setup(settings)

    def setup(self, settings):
        self.setTitle("Packing Groups")
        self.description = (
            "Packing groups define which texture maps should be packed into one file. "
            "You may choose which channels these textures will populate. "
            "The identifier signifies what letters to use to identify this new file "
            'e.g. "Identifier_AssetName.PNG".'
        )
        self.packing_groups_data = settings["packing_groups"]
        self.channels = ["Red", "Green", "Blue", "Alpha"]
        self.textures = [tex["name"] for tex in settings["textures"]]
        self.textures.insert(0, "Empty")
        self.fields = []

        self.description_text = QLabel(self.description, alignment=QtCore.Qt.AlignLeft)

        self.tw = QTreeWidget()
        self.tw.setAlternatingRowColors(False)
        self.tw.setHeaderLabels(
            ["Identifier", "Extension", "Red", "Green", "Blue", "Alpha"]
        )

        for group in self.packing_groups_data:
            data = [group["identifier"]] + [group["extension"]] + group["texture_types"]
            item = QTreeWidgetItem(self.tw, data)
            item.setData(0, QtCore.Qt.UserRole, group)

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
        item_data = {"identifier": i, "extension": e, "group": [r, g, b, a]}
        item = QTreeWidgetItem(self.tw, [i, e, r, g, b, a])
        item.setData(0, QtCore.Qt.UserRole, item_data)

    def on_remove_clicked(self):
        current = self.tw.currentItem()
        index = self.tw.indexOfTopLevelItem(current)
        self.tw.takeTopLevelItem(index)

    def get_data(self):
        data = []
        for i in range(self.tw.topLevelItemCount()):
            item_data = self.tw.topLevelItem(i).data(0, QtCore.Qt.UserRole)
            data.append(item_data)
        return data
