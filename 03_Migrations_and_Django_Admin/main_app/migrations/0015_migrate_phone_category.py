# Generated by Django 5.0.4 on 2025-02-07 10:50

from django.db import migrations

def set_phone_category(apps, schema_editor):
    phone_model = apps.get_model('main_app', 'Smartphone')

    all_phones = phone_model.objects.all()

    for phone in all_phones:
        if phone.price >= 750:
            phone.category = "Expensive"
        else:
            phone.category = "Cheap"

    phone_model.objects.bulk_update(all_phones, ['category'])


def set_phone_category_default(apps, schema_editor):
    phone_model = apps.get_model('main_app', 'Smartphone')

    all_phones = phone_model.objects.all()

    for phone in all_phones:
        phone.category = "No category"

    phone_model.objects.bulk_update(all_phones, ['category'])

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_migrate_phone_price'),
    ]

    operations = [
        migrations.RunPython(set_phone_category, set_phone_category_default)
    ]
