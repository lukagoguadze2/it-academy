import random
from datetime import datetime, timedelta

from faker import Faker
from models import (
    Author,
    Book,
    AuthorContainer,
    BookContainer
)


def generate_authors(n: int = 500) -> None:
    """Generate and save n random authors to the database."""
    fake = Faker()
    author_container = AuthorContainer()
    for _ in range(n):
        name = fake.first_name()
        last_name = fake.last_name()
        date_of_birth = fake.date_of_birth(minimum_age=20, maximum_age=80).strftime('%Y-%m-%d')
        place_of_birth = ' '.join(fake.location_on_land()[2:])
        author = Author(name, last_name, date_of_birth, place_of_birth)
        author_container.add_author(author)

    author_container.insert_authors_into_db()


def generate_books(n: int = 1000) -> None:
    """Generate and save n random books to the database."""
    fake = Faker()
    category_choices = ['Fiction', 'Science', 'History', 'Biography', 'Fantasy', 'Mystery', 'Romance', 'Horror']
    authors_data = AuthorContainer.get_all_author_ids_and_date_of_birth()
    author_ids: list[int] = list(authors_data.keys())
    books: BookContainer = BookContainer()
    for _ in range(n):
        name = fake.sentence(nb_words=3).rstrip('.')
        category_name = random.choice(category_choices)
        number_of_pages = fake.pyint(min_value=100, max_value=1000)
        author_id = random.choice(author_ids)

        # Generating valid date of issue
        date_of_issue = fake.date_between(
            start_date=authors_data[author_id] + timedelta(weeks=52 * 14),
            end_date=datetime.now()
        )
        book = Book(name, category_name, number_of_pages, date_of_issue, author_id)

        books.add_book(book)

    books.insert_books_into_db()
