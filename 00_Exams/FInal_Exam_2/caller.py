import os
from datetime import date

import django
from django.db.models import Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Label, Artist, Album

# Create queries within functions

def populate_db():
    # Clear existing data
    Label.objects.all().delete()
    Artist.objects.all().delete()
    Album.objects.all().delete()

    # Create Record Labels
    universal = Label.objects.create(
        name="Universal Music",
        headquarters="Hilversum, Netherlands",
        market_share=31.9
    )
    sony = Label.objects.create(
        name="Sony Music",
        headquarters="New York, USA",
        market_share=22.1
    )
    warner = Label.objects.create(
        name="Warner Music Group",
        headquarters="New York, USA",
        market_share=16.0
    )
    independent = Label.objects.create(
        name="Independent Records",
        headquarters="London, UK",
        market_share=2.5
    )
    polygram = Label.objects.create(
        name="PolyGram",
        headquarters="Not specified",
        market_share=0.0
    )

    # Create Artists
    adele = Artist.objects.create(
        name="Adele",
        nationality="GBR",
        awards=21
    )
    drake = Artist.objects.create(
        name="Drake",
        nationality="CAN",
        awards=15
    )
    bts = Artist.objects.create(
        name="BTS",
        nationality="KOR",
        awards=15
    )
    ed_sheeran = Artist.objects.create(
        name="Ed Sheeran",
        nationality="GBR",
        awards=20
    )
    newcomer = Artist.objects.create(
        name="Newcomer Artist",
        nationality="USA",
        awards=0
    )

    # Create Albums
    album1 = Album.objects.create(
        title="25",
        release_date=date(2015, 11, 20),
        description="Adele's third studio album",
        type="Soundtrack",
        is_hit=True,
        label=sony
    )
    album1.artists.add(adele)

    album2 = Album.objects.create(
        title="Scorpion",
        release_date=date(2018, 10, 29),
        description="Drake's double album",
        type="Remix",
        is_hit=True,
        label=universal
    )
    album2.artists.add(drake)

    album3 = Album.objects.create(
        title="BE",
        release_date=date(2020, 11, 20),
        description="BTS's self-produced album",
        type="Single",
        is_hit=True,
        label=warner
    )
    album3.artists.add(bts, newcomer)

    album4 = Album.objects.create(
        title="÷ (Divide)",
        release_date=date(2017, 3, 3),
        description="Ed Sheeran's chart-topping album",
        type="Other",
        is_hit=True,
        label=sony
    )
    album4.artists.add(ed_sheeran)

    album5 = Album.objects.create(
        title="Unknown Album",
        type="Other",
        is_hit=False,
        label=independent
    )
    album5.artists.add(ed_sheeran, adele)
# --------------------------
# populate_db()
# --------------------------
# print(Label.objects.get_labels_by_albums_count())
# --------------------------
def get_labels(search_string=None):
    if search_string is None:
        return "No search."

    labels = Label.objects.filter(name__icontains=search_string)

    if not labels.exists():
        return "No labels match this search."

    labels = labels.order_by('-market_share', 'name')

    result = []
    for label in labels:
        market_share_rounded = int(label.market_share)
        result.append(
            f"Label: {label.name}, headquarters: {label.headquarters}, "
            f"market share: {market_share_rounded}%"
        )

    return '\n'.join(result)
# --------------------------
# print(get_labels(search_string=''))
# print(get_labels(search_string=None))
# print(get_labels(search_string='nonexistent'))
# --------------------------
def get_best_label():
    labels = Label.objects.annotate(num_of_albums=Count('albums')).order_by('-num_of_albums', 'name')

    if not labels.exists():
        return "No data."

    best_label = labels.first()
    return f"The best label is {best_label.name} with {best_label.num_of_albums} albums."
# --------------------------
# print(get_best_label())
# --------------------------
def get_artists_by_albums_count():
    artists = Artist.objects.annotate(
        num_albums=Count('artists')
    ).order_by('-num_albums', 'name')[:3]

    if not artists.exists():
        return "No data."

    result = []
    for artist in artists:
        result.append(f"{artist.name}: {artist.num_albums} album/s.")

    return '\n'.join(result)
# --------------------------
# print(get_artists_by_albums_count())
# --------------------------
def get_most_productive_artist():
    top_artist = Artist.objects.annotate(
        num_albums=Count('artists')
    ).order_by('-num_albums', 'name').first()

    if not top_artist or top_artist.num_albums == 0:
        return "No data."

    albums = top_artist.artists.all().order_by('title')
    album_titles = [album.title for album in albums]
    titles_string = ", ".join(album_titles)

    return f"The most productive artist is {top_artist.name} with album titles: {titles_string}."
# --------------------------
# print(get_most_productive_artist())
# --------------------------
def get_latest_hit_album():
    latest_hit = Album.objects.filter(
        is_hit=True
    ).order_by('-release_date', 'title').first()

    if not latest_hit:
        return "No data."

    artists = latest_hit.artists.all().order_by('name')

    if artists.exists():
        artist_names = ", ".join([artist.name for artist in artists])
    else:
        artist_names = "TBA"

    return (
        f"The latest hit album is {latest_hit.title}, "
        f"type: {latest_hit.type}, "
        f"artists: {artist_names}."
    )
# --------------------------
# print(get_latest_hit_album())
# --------------------------
def award_album(album_title: str):
    try:
        album = Album.objects.get(title=album_title)
        artists = album.artists.all()

        if not artists.exists():
            return "Updates not applicable."

        updated_count = artists.update(awards=F('awards') + 1)

        return f"Updated awards for {updated_count} artist/s."

    except Album.DoesNotExist:
        return "Updates not applicable."
# --------------------------
# print(award_album('Nonexistent'))
# print(award_album('BE'))
# --------------------------