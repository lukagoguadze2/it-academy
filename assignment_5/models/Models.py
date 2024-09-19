from .BaseModels import (
    AuthorBase,
    BookBase,
)

from datetime import datetime
from datetime import date as datetime_date
from typing import Optional

from config import DATABASE_PATH
from utils.database import DatabaseManager


class Author(AuthorBase):
    def __init__(
            self,
            name: Optional[str] = None,
            last_name: Optional[str] = None,
            date_of_birth: Optional[str | datetime | datetime_date] = None,
            place_of_birth: Optional[str] = None,
            _id: Optional[int] = None
    ):
        super().__init__(
            name=name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            place_of_birth=place_of_birth
        )

        self.validate()

    def save(self):
        with DatabaseManager(DATABASE_PATH) as cursor:
            cursor.execute('''
                INSERT INTO author (name, last_name, date_of_birth, place_of_birth)
                VALUES (?, ?, ?, ?)
            ''', (self.name, self.last_name, self.date_of_birth, self.place_of_birth))

    def __str__(self):
        return f"Name: {self.name}\n"\
               f"Last Name: {self.last_name}\n"\
               f"Date: {self.date_of_birth}\n"\
               f"Place: {self.place_of_birth}"


class Book(BookBase):
    def __init__(
            self,
            name: Optional[str] = None,
            category_name: Optional[str] = None,
            number_of_pages: int = 0,
            date_of_issue: Optional[str | datetime | datetime_date] = None,
            author_id: Optional[int] = None,
            _id: Optional[int] = None
    ):
        super().__init__(
            name=name,
            category_name=category_name,
            number_of_pages=number_of_pages,
            date_of_issue=date_of_issue,
            author_id=author_id
        )

        self.__id = _id

        self.validate()

    @property
    def _id(self):
        return self.__id

    def save(self):
        with DatabaseManager(DATABASE_PATH) as cursor:
            cursor.execute('''
            INSERT INTO book (name, category_name, number_of_pages, date_of_issue, author_id)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.name, self.category_name, self.number_of_pages, self.date_of_issue, self.author_id))

    def __str__(self):
        return f'{'Id: ' + str(self._id) + '\n' if self._id else ''}'\
               f'Name: {self.name}\n'\
               f'Category: {self.category_name}\n'\
               f'Number of pages: {self.number_of_pages}\n'\
               f'Date of issue: {self.date_of_issue}\n'\
               f'Author ID: {self.author_id}'
