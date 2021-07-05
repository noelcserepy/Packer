from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from db.alchemy import DatabaseHandler


class MainTable(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        dbh = DatabaseHandler()
        all_pgs = dbh.get_all_packing_groups_ordered() 
        self.asset_table = QTableWidget(len(all_pgs), 5)
        self.asset_table.verticalHeader().setVisible(False)
        self.asset_table.horizontalHeader().setSectionResizeMode(
            QHeaderView(Qt.Orientation.Horizontal).Stretch
        )
        self.asset_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.asset_table.setHorizontalHeaderLabels(
            ["Asset Name", "Packing Group", "Output Path", "Date Modified", "Status"]
        )

        for i, pg in enumerate(all_pgs):
            self.asset_table.setItem(i, 0, QTableWidgetItem(pg.Asset.name))
            self.asset_table.setItem(i, 1, QTableWidgetItem(pg.PackingGroup.identifier))
            self.asset_table.setItem(i, 2, QTableWidgetItem(pg.Asset.directory))
            self.asset_table.setItem(
                i,
                3,
                QTableWidgetItem(pg.PackingGroup.date.strftime("%m/%d/%Y, %H:%M:%S")),
            )
            self.asset_table.setItem(i, 4, QTableWidgetItem(pg.PackingGroup.status))

        self.asset_table.setRowCount(len(all_pgs))
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.asset_table)