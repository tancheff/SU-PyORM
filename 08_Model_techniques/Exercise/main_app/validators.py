from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidateName:
    def __init__(self, message: str):
        self.message = message

    def __call__(self, value):
        for char in value:
            if not (char.isalpha() or char.isspace()):
                raise ValidationError(message=self.message)


@deconstructible
class ValidPhone:
    def __init__(self, message: str):
        self.message = message

    def __call__(self, value):
        if not value.startswith('+359') or not len(value) == 13 or  value[4:].isdigit():
            raise ValidationError(message=self.message)


# validator = ValidPhone("Phone number must start with '+359' followed by 9 digits")
# validator('+359123456789')  # No error
# validator('359123456789')    # Missing '+'
# validator('+35912345678')    # Too short
# validator('+3591234567890')  # Too long
# validator('+35912345678z')   # Contains non-digit character
