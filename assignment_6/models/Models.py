from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


author_book_table = Table(
    'author_book',
    Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True)
)

# Models
class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    birth_place = Column(String, nullable=False)
    books = relationship('Book', secondary=author_book_table, back_populates='authors')

    def __str__(self):
        return f"Id: {self.id}\n"\
               f"Name: {self.first_name}\n"\
               f"Last Name: {self.last_name}\n"\
               f"Date: {self.birth_date}\n"\
               f"Birth Place: {self.birth_place}"


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    publish_date = Column(Date, nullable=False)
    authors = relationship('Author', secondary=author_book_table, back_populates='books')

    def __str__(self):
        return f"Id: {self.id}\n"\
               f"Title: {self.title}\n"\
               f"Category: {self.category}\n"\
               f"Pages: {self.pages}\n"\
               f"Publish Date: {self.publish_date}"
