import os
import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location


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














