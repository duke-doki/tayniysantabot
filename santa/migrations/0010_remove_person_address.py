# Generated by Django 5.0 on 2023-12-14 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('santa', '0009_remove_person_phonenumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='address',
        ),
    ]
