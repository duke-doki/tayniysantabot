# Generated by Django 5.0 on 2023-12-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santa', '0013_person_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='chat_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='id персоны'),
        ),
    ]
