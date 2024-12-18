from importlib.metadata import requires

from django.db import models

# creating venv
# python3 -m venv ./venv
# for mac/linux source ./venv/bin/activate
# for windows venv\Scripts\activate

# zip project
# tar.exe -a -cf project.zip main_app orm_skeleton caller.py manage.py requirements.txt

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.PositiveIntegerField()

class Blog(models.Model):
    post = models.TextField()
    author = models.CharField(max_length=35)

class WeatherForecast(models.Model):
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    precipitation = models.FloatField()

class Recipe(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    ingredients = models.TextField()
    cook_time = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # auto_now=True
    # - on creation: the field is populated with current timestamp.
    # - on update: the field is updated to current timestamp each time .save() is called.
    # използва се за следене на последната промяна
    # за колона updated_at

    # auto_now_add=True
    # - on creation: the field is populated with the current timestamp.
    # - on update: the field remains unchanged.
    # използва се само за взимане на дата при създаване

class Product(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    username = models.CharField(max_length=65, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True, default="students@softuni.bg")
    bio = models.TextField(max_length=120)
    profile_image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=20)
    duration_minutes = models.PositiveIntegerField()
    equipment = models.CharField(max_length=90)
    calories_burned = models.PositiveIntegerField(default=1)
    is_favorite = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, null=True)

    # blank=True
    # - аllows the field to be empty in forms.
    # - you can set a default value and won't be null in DB

    # null=True
    # - аllows the field to store NULL in the database.

# class Book(models.Model):
#     GENRE_CHOICES = (
#         ("Fiction", "Fiction"),
#         ("Non-Fiction", "Non-Fiction"),
#         ("Science Fiction", "Science Fiction"),
#         ("Horror", "Horror")
#     )
#     genre = models.CharField(max_length=20, choices=GENRE_CHOICES)

class GenreChoices(models.TextChoices):
    FICTION = "Fiction", "Fiction"
    NON_FICTION = "Non-Fiction", "Non-Fiction"
    SCIENCE_FICTION = "Science Fiction", "Science Fiction"
    HORROR = "Horror", "Horror"

class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=GenreChoices.choices)
    publication_date = models.DateField(auto_now_add=True, editable=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title
