from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QTableView
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord, QSqlRelationalTableModel, QSqlTableModel
from db.alchemy import DatabaseHandler


class MainTable(QTableView):
    def __init__(self):
        super().__init__()
        self.setup2()

    def setup(self):
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
        self.add_content(all_pgs)
    
    def setup2(self):
        db = self.connect_to_database()
        model = QSqlTableModel(db=db)
        self.setModel(model)
        self.show()
        # self.setRowCount(len(all_pgs))
        # self.setColumnCount(5)
        # self.verticalHeader().setVisible(False)
        # self.horizontalHeader().setSectionResizeMode(
        #     QHeaderView(Qt.Orientation.Horizontal).Stretch
        # )
        # self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # self.setHorizontalHeaderLabels(
        #     ["Asset Name", "Packing Group", "Output Path", "Date Modified", "Status"]
        # )
        # self.add_content(all_pgs)

    def connect_to_database(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setHostName("packer")
        db.setDatabaseName("db/packer.db")
        db.setUserName("packer")
        db.setPassword("packer")
        ok = db.open()
        print(ok)
        print(db.tables())
        return db

    def add_content(self, all_pgs=None):
        if not all_pgs:
            dbh = DatabaseHandler()
            all_pgs = dbh.get_all_packing_groups_ordered()
        for i, pg in enumerate(all_pgs):
            self.setItem(i, 0, QTableWidgetItem(pg.Asset.name))
            self.setItem(i, 1, QTableWidgetItem(pg.PackingGroup.identifier))
            self.setItem(i, 2, QTableWidgetItem(pg.Asset.directory))
            self.setItem(
                i,
                3,
                QTableWidgetItem(pg.PackingGroup.date.strftime("%m/%d/%Y, %H:%M:%S")),
            )
            self.setItem(i, 4, QTableWidgetItem(pg.PackingGroup.status))

    def clear_content(self):
        self.clearContents()


