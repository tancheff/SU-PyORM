import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book

# Create queries within functions

# ------------- 1. Library -------------
def show_all_authors_with_their_books() -> str:
    all_authors = Author.objects.all().order_by('id')
    authors_with_books = []

    for author in all_authors:
        books = Book.objects.all().filter(author=author)

        if not books:
            continue

        titles = ", ".join(b.title for b in books)
        authors_with_books.append(f"{author.name} has written - {titles}!")

    return "\n".join(authors_with_books)

def delete_all_authors_without_books() -> None:
    # става само с 1 заявка:
    Author.objects.filter(book__isnull=True).delete()

delete_all_authors_without_books()

# print(Author.objects.get(name='George Orwell').book_set.exists())

# def delete_all_authors_without_books() -> None:
#     Author.objects.filter(author.book_set()='None').delete()

# # Create authors
# author1 = Author.objects.create(name="J.K. Rowling")
# author2 = Author.objects.create(name="George Orwell")
# author3 = Author.objects.create(name="Harper Lee")
# author4 = Author.objects.create(name="Mark Twain")
#
# # Create books associated with the authors
# book1 = Book.objects.create(
#     title="Harry Potter and the Philosopher's Stone",
#     price=19.99,
#     author=author1
# )
# book2 = Book.objects.create(
#     title="1984",
#     price=14.99,
#     author=author2
# )
#
# book3 = Book.objects.create(
#     title="To Kill a Mockingbird",
#     price=12.99,
#     author=author3
# )

# # Display authors and their books
# authors_with_books = show_all_authors_with_their_books()
# print(authors_with_books)
#
# # Delete authors without books
# delete_all_authors_without_books()
# print(Author.objects.count())
