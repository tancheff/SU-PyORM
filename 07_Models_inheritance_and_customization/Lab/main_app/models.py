from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
# from django.db.models.functions import datetime


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

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self) -> int:
        today = date.today()
        age = today.year - self.birth_date.year

        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1

        return age


class Mammal(Animal):
    fur_color = models.CharField(max_length=50)

class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)

class Reptile(Animal):
    scale_type = models.CharField(max_length=50)

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

        if self.specialty not in self.Specialities:
            raise ValidationError("Specialty must be a valid choice.")


class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = (
            (True, "Available"),
            (False, "Not Available")
        )
        kwargs['default'] = True

        super().__init__(*args, **kwargs)


class Veterinarian(EmployeeBaseClass):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()

    def is_available(self) -> bool:
        return self.availability


class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True

    def display_info(self) -> str:
        return (f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. "
                f"It makes a noise like '{self.sound}'.")

    def is_endangered(self) -> str:
        if self.species in ["Cross River Gorilla", "Orangutan", "Green Turtle"]:
            return f"{self.species} is at risk!"

        return f"{self.species} is not at risk."
