import os
from datetime import datetime

import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Publisher, Author, Book

# Create queries within functions
"""
# Publishers

1.	"Epic Reads," a U.S. publisher founded in 1923(15th of May) with an exceptional rating of 4.94.
2.	"Global Prints," an Australian publishing house, no established date or rating is provided.
3.	"Abrams Books," a publisher with a rating of 1.05, no country or established date is provided.

# Authors

1.	Jack London, a celebrated U.S. author born in 1876(12th of January), not active.
2.	Craig Richardson is a promising contemporary author, no additional info is provided.
3.	Ramsey Hamilton is recognized for his expertise in technical and specialized topics. No additional info is provided.
4.	Luciano Ramalho, a distinguished writer, is known for producing highly impactful educational works. No additional info is provided.

# Books

1.	"Adventures in Python" is an engaging and detailed guide to mastering a popular programming language. It was released in 2015(1st of June) by "Epic Reads," written by Craig Richardson, with additional contributions by Ramsey Hamilton. It has a high evaluation of 4.8 and is priced at $49.99.
2.	"The Call of the Wild," a classic fiction adventure story set during the Klondike Gold Rush, was published in 1903(23rd of November) by "Global Prints." Jack London penned it and achieved bestseller status with an excellent rating of 4.9, priced at $29.99.
3.	"Django World" is a non-fiction comprehensive resource for advanced users of a web development framework. Published in 2025(1st of January) by "Epic Reads," it was authored by Craig Richardson with collaborative efforts from Luciano Ramalho and Ramsey Hamilton. It has a perfect rating of 5.0 and is priced at $89.99.
4.	"Integration Testing," a non-fiction thorough exploration of expert-level testing strategies, was released in 2024(31st of December) by "Epic Reads." It is a bestseller authored by Ramsey Hamilton, earning a high rating of 4.89 and priced at $89.99.
5.	"Unit Testing" is a non-fiction detailed guide to foundational testing principles, published in 2025(1st of February) by "Epic Reads." Written by Craig Richardson with contributions from Ramsey Hamilton, it has a solid rating of 3.99 and is priced at $90.00.
"""
def populate_db():
# ------------- Publishers -------------
    epic_reads = Publisher.objects.create(
        name="Epic Reads",
        established_date=datetime.strptime('1923-05-15', '%Y-%m-%d').date(),
        country='U.S.',
        rating=4.94,
    )

    global_prints = Publisher.objects.create(
        name="Global Prints",
        country='Australia',
    )

    abram_books = Publisher.objects.create(
        name="Abrams Books",
        rating=1.05,
    )
# ------------- Authors -------------
    jack_london = Author.objects.create(
        name="Jack London",
        birth_date=datetime.strptime('1876-01-12', '%Y-%m-%d').date(),
        country='U.S.',
        is_active=False,
    )

    craig_richardson = Author.objects.create(
        name="Craig Richardson",
    )

    ramsey_hamilton = Author.objects.create(
        name="Ramsey Hamilton",
    )


    luciano_ramalho = Author.objects.create(
        name="Luciano Ramalho",
    )

# ------------- Books -------------
    book1 = Book.objects.create(
        title='Adventures in Python',
        publication_date=datetime.strptime('2015-06-01', '%Y-%m-%d').date(),
        # summary='engaging and detailed guide to mastering a popular programming language',
        # genre=
        price=49.99,
        rating=4.8,
        # is_bestseller=
        # updated_at=
        publisher=epic_reads,
        main_author=craig_richardson,
        # co_authors=ramsey_hamilton
    )
    book1.co_authors.add(ramsey_hamilton)

    book2 = Book.objects.create(
        title='The Call of the Wild',
        publication_date=datetime.strptime('1903-11-23', '%Y-%m-%d').date(),
        summary='a classic fiction adventure story set during the Klondike Gold Rush',
        genre='Fiction',
        price=29.99,
        rating=4.9,
        is_bestseller=True,
        # updated_at=
        publisher=global_prints,
        main_author=jack_london,
        # co_authors=''
    )


    book3 = Book.objects.create(
        title='Django World',
        publication_date='2025-01-01',
        summary='Comprehensive Django resource',
        genre='Non-Fiction',
        price=89.99,
        rating=5.0,
        # is_bestseller=
        # updated_at=
        publisher=epic_reads,
        main_author=craig_richardson,
        # co_authors=''
    )
    book3.co_authors.add(ramsey_hamilton, luciano_ramalho)
# --------------------------
# populate_db()
# --------------------------
# print(Publisher.objects.get_publishers_by_books_count())
# --------------------------
def get_publishers(search_string=None):
    if search_string is None:
        return "No search criteria."

    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string) | Q(country__icontains=search_string)).order_by('-rating', 'name')

    if not publishers.exists():
        return "No publishers found."

    ordered_publishers = []

    for publisher in publishers:
        ordered_publishers.append(
            f"Publisher: {publisher.name}, "
            f"country: {'Unknown' if publisher.country == 'TBC' else publisher.country}, "
            f"rating: {publisher.rating:.1f}"
        )

    return "\n".join(ordered_publishers)
# --------------------------
# print(get_publishers(""))
# --------------------------
def get_top_publisher():
    top_publisher = Publisher.objects.get_publishers_by_books_count().first()

    if not top_publisher:
        return "No publishers found."

    return f"Top Publisher: {top_publisher.name} with {top_publisher.books_count} books."
# --------------------------
# print(get_top_publisher())
# --------------------------
def get_top_main_author():
    # Get top author with annotated fields
    top_author = (Author.objects.annotate(
        books_count=Count('authored_books'),
        books_avg=Avg('authored_books__rating')
    ).order_by('-books_count', 'name').first())

    if not top_author or not top_author.books_count:
        return "No results."

    book_titles = (top_author.authored_books.order_by('title').values_list('title', flat=True))

    avg_rating = top_author.books_avg

    return f"Top Author: {top_author.name}, own book titles: {', '.join(book_titles)}, books average rating: {avg_rating:.1f}"
# --------------------------
# print(get_top_main_author())
# --------------------------
def get_authors_by_books_count():
    authors = Author.objects.annotate(
        total_books=Count('authored_books', distinct=True)
                    + Count('co_authored_books', distinct=True)
    ).order_by('-total_books', 'name')[:3]

    if not authors or sum(author.total_books for author in authors) == 0:
        return "No results."

    results = []

    for author in authors:
        results.append(f"{author.name} authored {author.total_books} books.")

    return "\n".join(results)
# --------------------------
print(get_authors_by_books_count())
# --------------------------
def get_top_bestseller():
    bestseller = Book.objects.filter(is_bestseller=True).order_by('-rating', 'title').first()

    if not bestseller:
        return "No results."

    co_authors = bestseller.co_authors.order_by('name').values_list('name', flat=True)
    co_authors = ", ".join(co_authors) if co_authors else 'N/A'

    return (f"Top bestseller: {bestseller.title}, rating: {bestseller.rating:.1f}. "
            f"Main author: {bestseller.main_author.name}. "
            f"Co-authors: {co_authors}.")
# --------------------------
# print(get_top_bestseller())
# --------------------------
def increase_price():
    books = Book.objects.filter(publication_date__year=2025, rating__gte=4.0).update(price=F('price')*1.2)

    if books == 0:
        return "No changes in price."

    return f"Prices increased for {books} books."
# --------------------------
# print(increase_price())
# --------------------------

