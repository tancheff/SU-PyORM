from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.db import models

# Create your models here.

# ------------- custom manager -------------
class LabelManager(models.Manager):
    def get_labels_by_albums_count(self):
        return (self.get_queryset().annotate(albums_count=models.Count('albums'))
                .order_by('-albums_count', 'name'))

# ------------- models -------------
class Label(models.Model):
    name = models.CharField(max_length=140, validators=[MinLengthValidator(2)])
    headquarters = models.CharField(max_length=150, default='Not specified')
    market_share = models.FloatField(default=0.1, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    created_at = models.DateTimeField(auto_now_add=True)

    objects = LabelManager()

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=140, validators=[MinLengthValidator(2)])
    nationality = models.CharField(max_length=3, validators=[MinLengthValidator(3), MaxLengthValidator(3)])
    awards = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Soundtrack', 'Soundtrack'),
        ('Remix', 'Remix'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=150, validators=[MinLengthValidator(1), MaxLengthValidator(150)])
    release_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, default='Other', validators=[MaxLengthValidator(10)],choices=TYPE_CHOICES)
    is_hit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    label = models.ForeignKey(to=Label, on_delete=models.SET_NULL, null=True, blank=True, related_name='albums')
    artists = models.ManyToManyField(to=Artist, related_name='artists')

    def __str__(self):
        return self.title
