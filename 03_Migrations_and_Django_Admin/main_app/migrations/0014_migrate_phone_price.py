# Generated by Django 5.0.4 on 2025-02-07 10:42

from django.db import migrations

def get_phone_price(apps, schema_editor):
    phone_model = apps.get_model('main_app', 'Smartphone')

    all_phones = phone_model.objects.all()

    for phone in all_phones:
        phone_price = len(phone.brand) * 5

def get_phone_price_default(apps, schema_editor):
    phone_model = apps.get_model('main_app', 'Smartphone')

    all_phones = phone_model.objects.all()

    for phone in all_phones:
        phone.price = 0

    phone_model.objects.bulk_update(all_phones, ['price'])

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_smartphone'),
    ]

    operations = [
        migrations.RunPython(get_phone_price, get_phone_price_default)
    ]
