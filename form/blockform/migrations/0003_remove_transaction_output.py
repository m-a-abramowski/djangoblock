# Generated by Django 2.0.5 on 2018-05-13 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blockform', '0002_address_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='output',
        ),
    ]
