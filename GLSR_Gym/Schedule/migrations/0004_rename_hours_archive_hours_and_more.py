# Generated by Django 5.1 on 2024-09-04 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0003_archive'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archive',
            old_name='Hours',
            new_name='hours',
        ),
        migrations.RenameField(
            model_name='archive',
            old_name='Users',
            new_name='users',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='Hours',
            new_name='hours',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='Users',
            new_name='users',
        ),
    ]
