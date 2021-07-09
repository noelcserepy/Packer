from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord, QSqlTableModel
from db.alchemy import DatabaseHandler


class MainTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        connect_to_database()
        dbh = DatabaseHandler()
        all_pgs = dbh.get_all_packing_groups_ordered()
        self.setRowCount(len(all_pgs))
        self.setColumnCount(5)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView(Qt.Orientation.Horizontal).Stretch
        )
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.setHorizontalHeaderLabels(
            ["Asset Name", "Packing Group", "Output Path", "Date Modified", "Status"]
        )

        for i, pg in enumerate(all_pgs):
            self.setItem(i, 0, QTableWidgetItem(pg.Asset.name))
            self.setItem(i, 1, QTableWidgetItem(pg.PackingGroup.identifier))
            self.setItem(i, 2, QTableWidgetItem(pg.Asset.directory))
            self.setItem(i, 3, QTableWidgetItem(
                pg.PackingGroup.date.strftime("%m/%d/%Y, %H:%M:%S")
            ))
            self.setItem(i, 4, QTableWidgetItem(pg.PackingGroup.status))


def connect_to_database():
    database = QSqlDatabase.database()
    if not database.isValid():
        database = QSqlDatabase.addDatabase("QSQLITE")
        if not database.isValid():
            print("Cannot add database")

    database.setDatabaseName("db/packer.db")
    if not database.open():
        print("Cannot open database")