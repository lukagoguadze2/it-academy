from .Models import Author, Book
from utils.database import DatabaseManager
from typing import Optional
from datetime import datetime
from config import DATABASE_PATH


class AuthorContainer:
    def __init__(self):
        self.__authors = []

    @property
    def authors(self):
        return self.__authors

    def add_author(self, author: Author):
        """Adds an Author instance to the container."""
        self.__authors.append(author)

    def add_authors_bulk(self, authors: list[Author]):
        """Adds multiple Author instances to the container."""
        self.__authors.extend(authors)

    def fetch_all_authors_from_db(self):
        """Fetches all authors from the database and stores them in the container."""
        query = "SELECT * FROM author"

        with DatabaseManager(DATABASE_PATH) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            author = Author(
                _id=row[0],
                name=row[1],
                last_name=row[2],
                date_of_birth=row[3],
                place_of_birth=row[4]
            )
            self.add_author(author)

    def insert_authors_into_db(self, cursor=None):
        """Inserts all authors in the container into the database.

        If a cursor is passed, it will be used. Otherwise, a new connection will be opened.
        """
        if not self.authors:
            print("No authors to insert.")
            return

        query = """
            INSERT INTO author (name, last_name, date_of_birth, place_of_birth)
            VALUES (?, ?, ?, ?)
        """

        if cursor is None:
            # If no cursor is passed, open a new database connection
            with DatabaseManager(DATABASE_PATH) as cursor:
                for author in self.authors:
                    cursor.execute(query, (author.name, author.last_name, author.date_of_birth, author.place_of_birth))
        else:
            # Use the passed cursor
            for author in self.authors:
                cursor.execute(query, (author.name, author.last_name, author.date_of_birth, author.place_of_birth))

        print(f"Inserted {len(self.authors)} authors into the database.")

    @staticmethod
    def get_all_author_ids() -> list[int]:
        query = """
            SELECT id FROM author
        """
        with DatabaseManager(DATABASE_PATH) as cursor:
            cursor.execute(query)
            ids = [row[0] for row in cursor.fetchall()]

        return ids

    @staticmethod
    def get_all_author_ids_and_date_of_birth() -> dict[int, datetime]:
        """returns dict, key as id and value as datetime"""
        query = """
            SELECT id, date_of_birth FROM author
        """

        with DatabaseManager(DATABASE_PATH) as cursor:
            cursor.execute(query)
            data = {
                    row[0]: datetime(*list(map(lambda x: int(x), row[1].split('-')))) for row in cursor.fetchall()
                }

        return data

    @staticmethod
    def get_author_birth_date(_id: int) -> Optional[datetime]:
        with DatabaseManager(DATABASE_PATH) as cursor:
            date = cursor.execute("""
                    SELECT date_of_birth FROM author WHERE id = ?
                """, (_id,)).fetchone()

        if date is not None:
            return datetime(*list(map(lambda x: int(x), date[0].split('-'))))

    def clear(self):
        """Clears all stored authors in the container."""
        self.__authors = []


class BookContainer:
    def __init__(self):
        self.__books = []

    @property
    def books(self):
        return self.__books

    def add_book(self, book: Book):
        self.__books.append(book)

    def add_book_bulk(self, books: list[Book]):
        self.__books.extend(books)

    def fetch_all_books_from_db(self):
        """Fetches all books from the database and store them"""
        query = "SELECT * FROM book"

        with DatabaseManager(DATABASE_PATH) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            # book = Book(_id=row[0], *row[1:])
            book = Book(
                _id=row[0],
                name=row[1],
                category_name=row[2],
                number_of_pages=row[3],
                date_of_issue=row[4],
                author_id=row[5]
            )
            self.add_book(book)

    def insert_books_into_db(self, cursor=None):
        """Inserts all books in the container into the database.

        If a cursor is passed, it will be used. Otherwise, a new connection will be opened.
        """

        if not self.books:
            print("No books to insert.")
            return

        query = """
            INSERT INTO book (name, category_name, number_of_pages, date_of_issue, author_id)
            VALUES (?, ?, ?, ?, ?)
        """

        if cursor is None:
            with DatabaseManager(DATABASE_PATH) as cursor:
                for book in self.books:
                    cursor.execute(query, (
                        book.name,
                        book.category_name,
                        book.number_of_pages,
                        book.date_of_issue,
                        book.author_id
                    ))
        else:
            for book in self.books:
                cursor.execute(query, (
                    book.name,
                    book.category_name,
                    book.number_of_pages,
                    book.date_of_issue,
                    book.author_id
                ))

        print(f"Inserted {len(self.books)} books to the database.")
