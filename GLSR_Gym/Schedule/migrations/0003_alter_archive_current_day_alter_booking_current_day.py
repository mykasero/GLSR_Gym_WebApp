# Generated by Django 5.1 on 2024-09-13 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0002_alter_booking_current_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='current_day',
            field=models.DateField(db_column='Data'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='current_day',
            field=models.DateField(db_column='Data', help_text='Wpisz w formacie rok-miesiac-dzien (np. 2024-09-01)'),
        ),
    ]
