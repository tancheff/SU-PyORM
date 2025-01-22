from django.db import models

class Shoe(models.Model):
    brand = models.CharField(max_length=25)
    size = models.PositiveIntegerField()


class UniqueBrands(models.Model):
    brand = models.CharField(max_length=25, unique=True)

# създаваме таблица с уникални имена:
# makemigrations main_app --name migrate_unique_brands --empty