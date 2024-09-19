import sqlite3

from config import DATABASE_PATH


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def drop_all_tables(self):
        with self as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = cursor.fetchall()

            for table_name in tables:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
                    print(f"Dropped table: {table_name[0]}")
                except sqlite3.Error as e:
                    print(f"An error occurred while dropping table {table_name[0]}: {e}")


def initialize_database() -> None:
    """Create tables if they do not exist."""
    with DatabaseManager(DATABASE_PATH) as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            last_name TEXT,
            date_of_birth TEXT NOT NULL,
            place_of_birth TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_name TEXT NOT NULL,
            number_of_pages INTEGER NOT NULL,
            date_of_issue TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE SET NULL
        )
        ''')
