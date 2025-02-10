# Generated by Django 5.0.4 on 2025-02-07 11:12
from datetime import timedelta

from django.db import migrations

def set_status_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')

    all_orders = order_model.objects.all()

    for order in all_orders:
        if order.status == "Pending":
            order.delivery = order.order_date + timedelta(days=3)
        elif order.status == "Completed":
            order.warranty =  "24 months"

    order_model.objects.bulk_update(all_orders, ['delivery', 'warranty'])

    # do not delete inside a loop
    # Django doesn’t support modifying the DB while iterating over a queryset
    order_model.objects.filter(status="Canceled").delete()


def set_status_warranty_default(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')

    all_orders = order_model.objects.all()

    for order in all_orders:
        order.warranty = "No warranty"
        order.delivery = ""

    order_model.objects.bulk_update(order_model, ['warranty', 'delivery'])

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_order'),
    ]

    operations = [
        migrations.RunPython(set_status_warranty, set_status_warranty_default)
    ]
