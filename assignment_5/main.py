import sys

from models import Author, Book
from config import BASE_DIR, DATABASE_PATH
from fake import generate_authors, generate_books
from utils.database import DatabaseManager

from utils.database import initialize_database

sys.path.append(BASE_DIR)


def get_book_with_most_pages() -> Book | None:
    with DatabaseManager(DATABASE_PATH) as cursor:
        cursor.execute("""
            SELECT * FROM book
            ORDER BY number_of_pages DESC
            LIMIT 1;
        """)

        book = cursor.fetchone()
        if book is not None:
            return Book(_id=book[0], *book[1:])


def get_average_number_of_pages() -> float | None:
    with DatabaseManager(DATABASE_PATH) as cursor:
        # Query to find the average number of pages
        cursor.execute("""
            SELECT AVG(number_of_pages) FROM book;
        """)

        # Fetch the result
        average_pages = cursor.fetchone()

        # Print the average number of pages
        if average_pages is not None:
            average_pages = average_pages[0]
            return round(average_pages, 2)


def get_youngest_author() -> Author | None:
    with DatabaseManager(DATABASE_PATH) as cursor:
        cursor.execute("""
            SELECT * FROM author
            ORDER BY date_of_birth DESC
            LIMIT 1;
        """)

        # Fetch the result
        youngest_author = cursor.fetchone()

        if youngest_author:
            return Author(_id=youngest_author[0], *youngest_author[1:])


def get_authors_without_books() -> list[Author] | None:
    with DatabaseManager(DATABASE_PATH) as cursor:
        # Query to find authors without books
        cursor.execute("""
            SELECT author.id, author.name, author.last_name, author.date_of_birth, author.place_of_birth
            FROM author
            LEFT JOIN book ON author.id = book.author_id
            WHERE book.author_id IS NULL;
        """)

        # Fetch all results
        authors_without_books = cursor.fetchall()

        if authors_without_books:
            return [Author(_id=author[0], *author[1:]) for author in authors_without_books]


def get_authors_with_more_than_three_books():
    with DatabaseManager(DATABASE_PATH) as cursor:
        # Query to find authors with more than 3 books
        cursor.execute("""
            SELECT author.id, author.name, author.last_name, author.date_of_birth, author.place_of_birth
            FROM author
            JOIN book ON author.id = book.author_id
            GROUP BY author.id
            HAVING COUNT(book.id) > 3
            LIMIT 5;
        """)

        # Fetch all results
        authors_with_more_than_three_books = cursor.fetchall()

        if authors_with_more_than_three_books:
            return [Author(_id=author[0], *author[1:]) for author in authors_with_more_than_three_books]


def main():
    db_manager = DatabaseManager(DATABASE_PATH)
    db_manager.drop_all_tables()

    initialize_database()

    # Adding authors
    generate_authors(500)

    # Adding books
    generate_books(1000)

    # Assignment
    book_with_most_pages = get_book_with_most_pages()
    if book_with_most_pages:
        print("\nBooks with most pages:")
        print(book_with_most_pages)
    else:
        print("Failed to find any books with most pages.")

    print()

    average_pages = get_average_number_of_pages()
    if average_pages is not None:
        print(f"Average number of pages: {average_pages:.2f}")
    else:
        print("Failed to calculate average number of pages.")

    print()
    youngest_author = get_youngest_author()
    if youngest_author:
        print("Youngest author:")
        print(youngest_author)
    else:
        print("Failed to calculate youngest author.")

    print()
    authors_without_books = get_authors_without_books()
    if authors_without_books:
        print("Authors without books:")
        for author in authors_without_books:
            print(author, end="\n\n")
    else:
        print("No authors without books.")

    print()
    authors_with_more_than_three_books = get_authors_with_more_than_three_books()
    if authors_with_more_than_three_books:
        print("Authors with more than three books:")
        for author in authors_with_more_than_three_books:
            print(author, end="\n\n")


if __name__ == "__main__":
    main()
