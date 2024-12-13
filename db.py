import sqlite3


class SQLiteManager:
    def __init__(self, db_name="settings.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value INTEGER
                )
            """
            )

    def insert_or_update(self, key, value):
        with self.conn:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO settings (key, value)
                VALUES (?, ?)
            """,
                (key, value),
            )
            self.conn.commit()

    def get_value(self, key):
        with self.conn:
            cursor = self.conn.execute(
                "SELECT value FROM settings WHERE key = ?", (key,)
            )
            row = cursor.fetchone()
            if row is None:
                default_values = {
                    "screen_type": 1,
                    "level": 1,
                    "music_volume": 0.2,
                }
                return default_values.get(key, None)
            return row[0]

    def close(self):
        self.conn.close()
