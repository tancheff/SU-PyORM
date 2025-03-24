from email.policy import default
from wsgiref.validate import validator

from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count

# Create your models here.
# ------------- custom manager -------------
class PublisherManager(models.Manager):
    def get_publishers_by_books_count(self):
        return self.get_queryset().annotate(books_count=Count('books')).order_by('-books_count', 'name')

# ------------- models -------------
class Publisher(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    established_date = models.DateField(default='1800-01-01')
    country = models.CharField(max_length=40, default='TBC', validators=[MaxLengthValidator(40)])
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    objects = PublisherManager()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3), MaxLengthValidator(100)])
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=40, default='TBC', validators=[MaxLengthValidator(40)])
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200, validators=[MinLengthValidator(2), MaxLengthValidator(200)])
    publication_date = models.DateField()
    summary = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=11, choices=GENRE_CHOICES, default='Other',
                             validators=[MaxLengthValidator(11)]
    )

    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.01,
                                validators=[
                                    MinValueValidator(0.01),
                                    MaxValueValidator(9999.99)
                                ]
    )
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    is_bestseller = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    publisher = models.ForeignKey(to=Publisher, on_delete=models.CASCADE, related_name='books')
    main_author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='authored_books')
    co_authors = models.ManyToManyField(to=Author, related_name='co_authored_books')

    def __str__(self):
        return self.title

