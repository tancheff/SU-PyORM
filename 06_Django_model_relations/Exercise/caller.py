import os
import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review


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

# ------------- 2. Music App -------------
def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)

    # също може и в обратен ред но с различни окончания:
    # song.artists.add(artist)

def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    artist = Artist.objects.get(name=artist_name)
    all_songs = artist.songs.all().order_by('-id')

    return all_songs

def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


# # Create artists
# artist1 = Artist.objects.create(name="Daniel Di Angelo")
# artist2 = Artist.objects.create(name="Indila")
# # Create songs
# song1 = Song.objects.create(title="Lose Face")
# song2 = Song.objects.create(title="Tourner Dans Le Vide")
# song3 = Song.objects.create(title="Loyalty")

# # Add a song to an artist
# add_song_to_artist("Daniel Di Angelo", "Lose Face")
# add_song_to_artist("Daniel Di Angelo", "Loyalty")
# add_song_to_artist("Indila", "Tourner Dans Le Vide")
#
# # Get all songs by a specific artist
# songs = get_songs_by_artist("Daniel Di Angelo")
# for song in songs:
#     print(f"Daniel Di Angelo: {song.title}")
#
# # Get all songs by a specific artist
# songs = get_songs_by_artist("Indila")
# for song in songs:
#     print(f"Indila: {song.title}")
#
# # Remove a song from an artist
# remove_song_from_artist("Daniel Di Angelo", "Lose Face")
# #
# # Check if the song is removed
# songs = get_songs_by_artist("Daniel Di Angelo")
# #
# for song in songs:
#     print(f"Songs by Daniel Di Angelo after removal: {song.title}")

# ------------- 3. Shop -------------
def calculate_average_rating_for_product_by_name(product_name: str) -> str:
    product = Product.objects.get(name=product_name)
    all_reviews = product.review_set.all()

    avg_rating = sum([r.rating for r in all_reviews])/len([r.rating for r in all_reviews])

    return f'{avg_rating:.1f}'


# # Create some products
# product1 = Product.objects.create(name="Laptop")
# product2 = Product.objects.create(name="Smartphone")
# product3 = Product.objects.create(name="Headphones")
# product4 = Product.objects.create(name="PlayStation 5")
#
# # Create some reviews for products
# review1 = Review.objects.create(description="Great laptop!", rating=5, product=product1)
# review2 = Review.objects.create(description="The laptop is slow!", rating=2, product=product1)
# review3 = Review.objects.create(description="Awesome smartphone!", rating=5, product=product2)

# Calculate and print the average rating
print(calculate_average_rating_for_product_by_name("Laptop"))













