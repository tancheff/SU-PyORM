from datetime import timedelta

from django.db import models

# Create your models here.

# ------------- 1. Library -------------
class Author(models.Model):
    name = models.CharField(max_length=40)

class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

# ------------- 2. Music App -------------
class Song(models.Model):
    title = models.CharField(max_length=100, unique=True)

    # def __str__(self):
    #     return f"Song's Title: {self.title}"

class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    songs = models.ManyToManyField(to=Song, related_name='artists')
    # вместо да пишем .artist_set, достъпваме всички артисти чрез .artists

# ------------- 3. Shop -------------
class Product(models.Model):
    name = models.CharField(max_length=100)

class Review(models.Model):
    description = models.TextField(max_length=200)
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='reviews')

# ------------- 4. License -------------
class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

class DrivingLicense(models.Model):
    license_number = models.CharField(max_length=10, unique=True)
    issue_date = models.DateField()
    driver = models.OneToOneField(to=Driver, on_delete=models.CASCADE, related_name='license') # driver_id is UNIQUE

    def __str__(self):
        expiration_date = self.issue_date + timedelta(days=365)
        return f"License with number: {self.license_number} expires on {expiration_date}!"

# ------------- 5. Car Registration -------------
class Owner(models.Model):
    name = models.CharField(max_length=50)

class Car(models.Model):
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    owner = models.ForeignKey(to=Owner, on_delete=models.CASCADE, related_name='cars', blank=True, null=True)

class Registration(models.Model):
    registration_number = models.CharField(max_length=10, unique=True)
    registration_date = models.DateField(blank=True, null=True)
    car = models.OneToOneField(to=Car, on_delete=models.CASCADE, related_name='registration', blank=True, null=True)
