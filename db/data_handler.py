import sqlite3



class DataHandler():
    def __init__(self):
        self.conn = sqlite3.connect("db/packer.db")
        self.conn.execute("PRAGMA foreign_keys = ON;")
        query = """
            CREATE TABLE IF NOT EXISTS packing_groups (
            packing_group_id INTEGER NOT NULL,
            asset_name TEXT,
            group_identifier TEXT,
            path TEXT,
            status TEXT NOT NULL,
            date TEXT,
            size INTEGER,
            channel_r_path TEXT,
            channel_g_path TEXT,
            channel_b_path TEXT,
            channel_a_path TEXT,
            PRIMARY KEY (packing_group_id));"""

        self.cur = self.conn.execute(query)


    def save_asset(self, asset_name, group_identifier, path, status, channel_r_path, 
                    channel_g_path, channel_b_path, channel_a_path, date=None, size=None):

        query = """
            INSERT INTO packing_groups (
                asset_name,
                group_identifier,
                path,
                status,
                date,
                size,
                channel_r_path,
                channel_g_path,
                channel_b_path,
                channel_a_path)
            VALUES (
                :asset_name,
                :group_identifier,
                :path,
                :status,
                :date,
                :size,
                :channel_r_path,
                :channel_g_path,
                :channel_b_path,
                :channel_a_path);"""

        argument_mapping = {
            "asset_name": asset_name,
            "group_identifier": group_identifier,
            "path": path,
            "status": status,
            "date": date,
            "size": size,
            "channel_r_path": channel_r_path,
            "channel_g_path": channel_g_path,
            "channel_b_path": channel_b_path,
            "channel_a_path": channel_a_path}

        with self.conn:
            self.cur.execute(query, argument_mapping)


    def get_all_rows(self):
        query = "SELECT asset_name, group_identifier, path, date, status FROM packing_groups ORDER BY asset_name"
        with self.conn:
            rows = []
            for row in self.cur.execute(query):
                rows.append(row)
            return rows 
