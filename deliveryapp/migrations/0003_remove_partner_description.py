# Generated by Django 3.1.7 on 2021-04-21 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliveryapp', '0002_order_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='description',
        ),
    ]
