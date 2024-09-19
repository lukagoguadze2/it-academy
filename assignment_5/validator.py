import sqlite3
from typing import Set


class AuthorValidator:
    def __init__(self):
        self.__valid_author_ids: Set[int] = set()
        self.__load_valid_author_ids()

    @property
    def valid_author_ids(self) -> Set[int]:
        return self.__valid_author_ids

    def __load_valid_author_ids(self):
        """Load valid author IDs into memory."""
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM author')
        self._valid_author_ids = set(row[0] for row in cursor.fetchall())
        conn.close()

    def is_valid_author_id(self, author_id: int) -> bool:
        """Check if the author ID is valid using cached data."""
        return author_id in self._valid_author_ids

    def update_author_cache(self):
        """Update the cache with the latest author IDs."""
        self.__load_valid_author_ids()
