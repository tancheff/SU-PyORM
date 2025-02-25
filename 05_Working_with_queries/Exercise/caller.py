import os
from typing import List
import django
from django.db.models import Case, When, Value


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# Create and check models
# Run and print your queries

from main_app.choices import OSChoices, LaptopBrandChoice

from main_app.models import ChessPlayer, Dungeon, Meal, Workout, ArtworkGallery, Laptop

# ------------- 1. Artwork Gallery -------------
def show_highest_rated_art() -> str:
    artwork = ArtworkGallery.objects.order_by('-rating', 'id').first()
    # SELECT * FROM artwork
    # ORDER BY rating DESC, id ASC
    # LIMIT 1;

    return f"{artwork.art_name} is the highest-rated art with a {artwork.rating} rating!"

def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])

def delete_negative_created_arts() -> None:
    ArtworkGallery.objects.filter(rating__lt=0).delete()

# artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)

# # Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())

# ------------- 2. Laptop -------------
def show_the_most_expensive_laptop() -> str:
    laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{laptop.brand} is the most expensive laptop available for {laptop.price}$!"

def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)

def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)

def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(memory=16)

def update_operation_systems() -> None:
    # само с 1 заявка:
    Laptop.objects.update(
        operation_system=Case(
            When(brand='Asus', then=Value(operation_system=OSChoices.WINDOWS)),
            When(brand='Apple', then=Value(operation_system=OSChoices.MACOS)),
            When(brand__in=['Dell', 'Acer'], then=Value(operation_system=OSChoices.LINUX)),
            When(brand='Lenovo', then=Value(operation_system=OSChoices.CHROME_OS)),
        )
    )

    # 4 отделни заявки:
    # Laptop.objects.filter(brand='Asus').update(operation_system='Windows')
    # Laptop.objects.filter(brand='Apple').update(opeartion_system='MacOS')
    # Laptop.objects.filter(brand__in=['Dell', 'Acer']).update(operation_system='Linux')
    # Laptop.objects.filter(brand='Lenovo').update(opeartion_system='Chrome OS')

def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()

# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )
#
# # Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
#
# # Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)

# update_to_512_GB_storage()
# update_to_16_GB_memory()
# update_operation_systems()
#
# # Retrieve 2 laptops from the database
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()
#
# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)

# ------------- 3. Chess Player -------------
def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)

def delete_chess_players() -> None:
    ChessPlayer.objects.filter(title='no title').delete()

def change_chess_games_won() -> None:
    ChessPlayer.objects.filter(title='GM').update(games_won=30)

def change_chess_games_lost() -> None:
    ChessPlayer.objects.filter(title__isnull=True).update(games_lost=25)

def change_chess_games_drawn() -> None:
    ChessPlayer.objects.update(games_drawn=10)

def grand_chess_title_GM() -> None:
    ChessPlayer.objects.filter(rating__range=2400).update(title='GM')

def grand_chess_title_IM() -> None:
    ChessPlayer.objects.filter(rating__range=[2300, 2399]).update(title='IM')

def grand_chess_title_FM() -> None:
    ChessPlayer.objects.filter(rating__range=[2200, 2299]).update(title='FM')

def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__lte=2199)


# player1 = ChessPlayer(
#     username='Player1',
#     title='no title',
#     rating=2200,
#     games_played=50,
#     games_won=20,
#     games_lost=25,
#     games_drawn=5,
# )
# player2 = ChessPlayer(
#     username='Player2',
#     title='IM',
#     rating=2350,
#     games_played=80,
#     games_won=40,
#     games_lost=25,
#     games_drawn=15,
# )

# # Call the bulk_create_chess_players function
# bulk_create_chess_players([player1, player2])

# # Call the delete_chess_players function
# delete_chess_players()
#
# # Check that the players are deleted
# print("Number of Chess Players after deletion:", ChessPlayer.objects.count())

# ------------- 4. Meal -------------
def set_new_chefs() -> None:
    # само с 1 заявка:
    Meal.objects.update(
        chef=Case(
            When(meal_type='Breakfast', then=Value('Gordon Ramsay')),
            When(meal_type='Lunch', then=Value('Julia Child')),
            When(meal_type='Dinner', then=Value('Jamie Oliver')),
            When(meal_type='Snack', then=Value('Thomas Keller')),

        )
    )

def set_new_preparation_times() -> None:
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type='Breakfast', then=Value('10 minutes')),
            When(meal_type='Lunch', then=Value('12 minutes')),
            When(meal_type='Dinner', then=Value('15 minutes')),
            When(meal_type='Snack', then=Value('5 minutes')),
        )
    )

def update_low_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=['Breakfast', 'Dinner']).update(calories=400)

def update_high_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).update(calories=700)

def delete_lunch_and_snack_meals() -> None:
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).delete()

# ------------- 5. Dungeon -------------
def show_hard_dungeons() -> str:
    hard_dungeons = Dungeon.objects.filter(difficulty='Hard').order_by('-location')

    result = [f"{d.name} is guarded by {d.boss_name} who has {d.boss_health} health points!" for d in hard_dungeons]

    return "\n".join(result)

def bulk_create_dungeons(args: List[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)

def update_dungeon_names() -> None:
    Dungeon.objects.update(
        name=Case(
            When(difficulty='Easy', then=Value('The Erased Thombs')),
            When(difficulty='Medium', then=Value('The Coral Labyrinth')),
            When(difficulty='Easy', then=Value('The Lost Haunt')),
        )
    )

def update_dungeon_bosses_health() -> None:
    Dungeon.objects.exclude(difficulty='Easy').update(boss_health=500)

def update_dungeon_recommended_levels():
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty='Easy', then=Value(25)),
            When(difficulty='Medium', then=Value(50)),
            When(difficulty='Hard', then=Value(75))
        )
    )

def update_dungeon_rewards() -> None:
    Dungeon.objects.update(
        rewards=Case(
            When(boss_health=500, then=Value('1000 Gold')),
            When(location__startswith='E', then=Value('New dungeon unlocked')),
            When(location__endswith='s', then=Value('Dragonheart Amulet'))
        )
    )

def set_new_locations() -> None:
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss')),
        )
    )
































