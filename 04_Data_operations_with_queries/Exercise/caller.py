import os
from typing import List

import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# Create queries within functions

# -------------------------- 1. Pet --------------------------
def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(name=name, species=species)

    # ако трябва да се сетва custom logic това е предпочитано за създаване
    # pet = Pet(name=name, species=species)
    # pet.save()

    return f"{pet.name} is a very cute {pet.species}!"

# ------------------------ 2. Artifact ------------------------
def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(name=name,
                                       origin=origin,
                                       age=age,
                                       description=description,
                                       is_magical=is_magical)

    return f"The artifact {artifact.name} is {artifact.age} years old!"

def rename_artifact(artifact: Artifact, new_name: str) -> None:
    # променяме всички записи, които отг. на това условие
    # Artifact.objects.filter(is_magical=True, age__gt=250).update(name=new_name)

    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name

        artifact.save()

def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()

# ------------------------ 3. Location ------------------------
def show_all_locations() -> str:
    location_model = Location.objects.all().order_by('-id')
    list_of_locations = [f"{l.name} has a population of {l.population}!" for l in location_model]

    return "\n".join(list_of_locations)

# --- helper method ---
# def create_new_location(name, region, population, description, is_capital) -> None:
#     location = Location.objects.create(name=name,
#                                        region=region,
#                                        population=population,
#                                        description=description,
#                                        is_capital=is_capital)
#
# create_new_location('Sofia','Sofia Region','1329000','The capital of Bulgaria and the largest city in the country','False')
# create_new_location('Plovdiv','Plovdiv Region','346942','The second-largest city in Bulgaria with a rich historical heritage','False')
# create_new_location('Varna','Varna Region','330486','A city known for its sea breeze and beautiful beaches on the Black Sea','False')


def new_capital() -> None:
    # location = Location.objects.first()     # SELECT * FROM locations LIMIT 1
    # location.is_capital = True
    # location.save()

    Location.objects.filter(pk=1).update(is_capital=True)

def get_capitals() -> QuerySet:
    return Location.objects.filter(is_capital=True).values('name')

def delete_first_location() -> None:
    Location.objects.filter(pk=1).delete()

# -------------------------- 4. Car --------------------------
# --- helper method ---
# def create_car(model, year, color, price) -> None:
#     car = Car.objects.create(model=model,
#               year=year,
#               color=color,
#               price=price)
#
# create_car('Mercedes C63 AMG','2019','white','120000.00')
# create_car('Audi Q7 S line','2023','black','183900.00')
# create_car('Chevrolet Corvette','2021','dark grey','199999.00')

def apply_discount() -> None:
    car_model = Car.objects.all()

    for car in car_model:
        car.price_with_discount = float(car.price) * (1 - car.percentage_from_year())
        # car.save()

    Car.objects.bulk_update(car_model, ['price_with_discount'])

def get_recent_cars():
    recent_cars = Car.objects.all().filter(year__gt=2000).values('model', 'price_with_discount')

    return recent_cars

def delete_last_car():
    Car.objects.last().delete()

# -------------------------- 5. Task --------------------------
def show_unfinished_tasks() -> str:
    unfinished_tasks = Task.objects.filter(is_finished=False)

    list_of_unfinished_tasks = []

    for task in unfinished_tasks:
        list_of_unfinished_tasks.append(f"Task - {task.title} needs to be done until {task.due_date}!")

    return "\n".join(list_of_unfinished_tasks)

def complete_odd_tasks():
    all_tasks = Task.objects.all()

    for task in all_tasks:
        if task.id % 2 == 1:
            task.is_finished=True

    Task.objects.bulk_update(all_tasks, ['is_finished'])

def encode_and_replace(text: str, task_title: str):
    new_description = ""

    for t in text:
        new_description += chr(ord(t) - 3)

    tasks_to_change = Task.objects.all().filter(title=task_title)

    for task in tasks_to_change:
        task.description = new_description
        # task.save()

    Task.objects.bulk_update(tasks_to_change, ['description'])

    # решение само с 1 заявка, вместо с 2:
    # Task.objects.filter(title=task_title).update(description=new_description)


# -------------------------- 5. Hotel Room --------------------------
# helper method:
# def create_hotel_room(room_number: int,room_type: str,capacity: int,amenities: str,price_per_night: float):
#
#     HotelRoom.objects.create(room_number=room_number,
#                       room_type=room_type,
#                       capacity=capacity,
#                       amenities=amenities,
#                       price_per_night=price_per_night)
#
# create_hotel_room(401,'Standard',2,'Tv',100.00)
# create_hotel_room(501,'Deluxe',3,'Wi-Fi',200.00)
# create_hotel_room(601,'Deluxe',6,'Jacuzzi',400.00)


def get_deluxe_rooms():
    all_deluxe_rooms = HotelRoom.objects.all().filter(room_type='Deluxe')

    list_of_rooms = []

    for room in all_deluxe_rooms:
        if room.id % 2 == 0:
            list_of_rooms.append(f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!")

    return '\n'.join(list_of_rooms)

def increase_room_capacity():
    all_rooms = HotelRoom.objects.all().order_by('id')

    for room in all_rooms:
        if not room.is_reserved:
            continue

        if room.id == all_rooms.first().id:
            room.capacity *= 2
            continue

        prev_room = HotelRoom.objects.filter(pk=(room.id-1))

        room.capacity += prev_room[0].capacity

    HotelRoom.objects.bulk_update(all_rooms, ['capacity'])

def reserve_first_room():
    HotelRoom.objects.filter(pk=1).update(is_reserved=True)
    # HotelRoom.objects.first().update(is_reserved=False)

def delete_last_room():
    last_room = HotelRoom.objects.last()
    if not last_room.is_reserved:
        HotelRoom.objects.last().delete()

# -------------------------- 5. Character --------------------------
# helper methods
# character1 = Character.objects.create(
#     name='Gandalf',
#     class_name='Mage',
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory='Staff of Magic, Spellbook',
# )
# character2 = Character.objects.create(
#     name='Hector',
#     class_name='Warrior',
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory='Sword of Troy, Shield of Protection',
# )

def update_characters() -> None:
    Character.objects.filter(class_name="Mage").update(level=3, )
    all_chars = Character.objects.all()

    for char in all_chars:
        if char.class_name == "Mage":
            char.level += 3
            char.intelligence -= 7
        elif char.class_name == "Warrior":
            char.hit_points /= 2
            char.dexterity += 4
        else:
            char.inventory = "The inventory is empty"

    Character.objects.bulk_update(all_chars,
                                  ['class_name', 'level', 'intelligence', 'hit_points', 'dexterity', 'inventory'])

def fuse_characters(first_character: Character, second_character: Character):
    inventory_item = ""

    if first_character.class_name == "Mage" or first_character.class_name == "Scout":
        inventory_item = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        inventory_item = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=f'{first_character.name} {second_character.name}',
        class_name='Fusion',
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=inventory_item,
        )

    first_character.delete()
    second_character.delete()

def grand_dexterity():
    all_characters = Character.objects.all()

    for char in all_characters:
        char.dexterity = 30

    Character.objects.bulk_update(all_characters, ['dexterity'])

def grand_intelligence():
    all_characters = Character.objects.all()

    for char in all_characters:
        char.intelligence = 40

    Character.objects.bulk_update(all_characters, ['intelligence'])

def grand_strength():
    all_characters = Character.objects.all()

    for char in all_characters:
        char.strength = 50

def delete_character():
    Character.objects.filter(inventory="").delete()


delete_character()
