from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Author, Book, Base, author_book_table

import random

engine = create_engine('sqlite:///library.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
faker = Faker()


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def create_random_authors(n: int):
    authors = []
    for _ in range(n):
        author = Author(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            birth_date=faker.date_of_birth(minimum_age=18, maximum_age=80),
            birth_place=faker.city()
        )
        authors.append(author)
    session.add_all(authors)
    session.commit()


def create_random_books(n: int, author_ids: list[int]):
    books = []
    for _ in range(n):
        book = Book(
            title=faker.sentence(nb_words=4),
            category=faker.word(),
            pages=random.randint(50, 1000),
            publish_date=faker.date_this_century()
        )
        session.add(book)

        random_authors = random.sample(author_ids, random.randint(1, 3))
        book.authors.extend(session.query(Author).filter(Author.id.in_(random_authors)).all())

        books.append(book)

    session.commit()
    return books


def find_book_with_most_pages():
    book = session.query(Book).order_by(Book.pages.desc()).first()
    print("Book with most pages:")
    print(book)
    print("Author(s):", end=" ")
    for author in book.authors:
        print(author.id, end=" ")
    print()


def calculate_average_pages():
    avg_pages = session.query(func.avg(Book.pages)).scalar()
    print(f"Average number of pages: {avg_pages}")


def find_youngest_author():
    youngest_author = session.query(Author).order_by(Author.birth_date.desc()).first()
    print(f"Youngest author")
    print(youngest_author)


def find_authors_without_books():
    authors_without_books = session.query(Author).outerjoin(author_book_table).filter(author_book_table.c.book_id == None).all()
    print("Authors without books:")
    for author in authors_without_books:
        print(f"{author.first_name} {author.last_name}")


def find_authors_with_more_than_3_books():
    authors = session.query(Author).join(author_book_table).group_by(Author.id).having(func.count(author_book_table.c.book_id) > 3).limit(5).all()
    print("Authors with more than 3 books:")
    for author in authors:
        print(author, end="\n\n")


def main():
    create_random_authors(500)
    author_ids = [author.id for author in session.query(Author).all()]
    create_random_books(1000, author_ids)

    find_book_with_most_pages()
    print()
    calculate_average_pages()
    print()
    find_youngest_author()
    print()
    find_authors_without_books()
    print()
    find_authors_with_more_than_3_books()


if __name__ == "__main__":
    main()
