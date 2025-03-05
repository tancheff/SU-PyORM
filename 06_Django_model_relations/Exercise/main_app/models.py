from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=40)

class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Song(models.Model):
    title = models.CharField(max_length=100, unique=True)

    # def __str__(self):
    #     return f"Song's Title: {self.title}"

class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    songs = models.ManyToManyField(to=Song, related_name='artists')
    # вместо да пишем .artist_set, достъпваме всички артисти чрез .artists

class Product(models.Model):
    name = models.CharField(max_length=100)

class Review(models.Model):
    description = models.TextField(max_length=200)
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='reviews')






















