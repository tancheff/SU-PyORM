from django.db import models

# Create your models here.

# # примерни класове, които да се наслеяват от всички таблици

# class TimeStampModel(models.Model):
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()
#
#     class Meta:
#         abstract = True

# class SoftDeleteModel(models.Model):
#     is_deleted = models.BooleanField(default=False)
#
#     class Meta:
#         abstract = True

# ------------- 1. Zoo Animals -------------
class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

class Mammal(Animal):
    fur_color = models.CharField(max_length=50)

class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)

class Reptile(Animal):
    scale_type = models.CharField(max_length=50)

# ------------- 2. Zoo Employees -------------
class EmployeeBaseClass(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True

SPECIALITIES = (
    ("Mammals", "Mammals"),
    ("Birds", "Birds"),
    ("Reptiles", "Reptiles"),
    ("Others", "Others")
)

class ZooKeeper(EmployeeBaseClass):
    class Specialities(models.TextChoices):
        Mammals = "Mammals"
        Birds = "Birds"
        Reptiles = "Reptiles"
        Others = "Others"

    specialty = models.CharField(max_length=10, choices=Specialities.choices)
    managed_animals = models.ManyToManyField(to='Animal')

    def clean(self):
        super().clean()

class Veterinarian(EmployeeBaseClass):
    license_number = models.CharField(max_length=10)

# ------------- 3. Animal Display System -------------
class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True