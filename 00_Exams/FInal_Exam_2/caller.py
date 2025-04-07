import os
from datetime import date

import django


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

populate_db()