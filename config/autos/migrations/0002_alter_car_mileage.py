# Generated by Django 4.1.4 on 2022-12-12 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='mileage',
            field=models.IntegerField(null=True),
        ),
    ]
