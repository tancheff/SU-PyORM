from django.core.exceptions import ValidationError


def validate_menu_categories(values):
    categories = ["Appetizers", "Main Course", "Desserts"]

    for category in categories:
        if category not in values:
            raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')

