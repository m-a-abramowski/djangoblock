# Generated by Django 2.0.5 on 2018-05-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockform', '0008_transaction_output'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='output',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]