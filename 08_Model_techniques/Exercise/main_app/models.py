from django.core.validators import MinValueValidator
from django.db import models

from main_app.validators import ValidateName, ValidPhone


# Create your models here.
# ------------- 1. Customer -------------
class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            ValidateName("Name can only contain letters and spaces")
        ]
    )
    age =  models.PositiveIntegerField(
        validators=[
            MinValueValidator(18, "Age must be greater than or equal to 18")
        ]
    )
    email = models.EmailField(
        error_messages={'invalid': "Enter a valid email address"}
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[
            ValidPhone("Phone number must start with '+359' followed by 9 digits")
        ]
    )
    website_url = models.URLField(
        error_messages={'invalid': "Enter a valid URL"}
    )

# ------------- 2. Media -------------
