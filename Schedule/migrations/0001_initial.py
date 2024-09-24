# Generated by Django 5.1 on 2024-09-07 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('users', models.CharField(db_column='Uzytkownicy', max_length=100)),
                ('users_amount', models.IntegerField(db_column='Ilosc osob')),
                ('start_hour', models.TimeField(db_column='Start')),
                ('end_hour', models.TimeField(db_column='Koniec')),
                ('current_day', models.DateTimeField(db_column='Data')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('users', models.CharField(db_column='Uzytkownicy', max_length=100)),
                ('users_amount', models.IntegerField(db_column='Ilosc_osob')),
                ('start_hour', models.TimeField(db_column='Start')),
                ('end_hour', models.TimeField(db_column='Koniec')),
                ('current_day', models.DateTimeField(db_column='Data')),
            ],
        ),
    ]