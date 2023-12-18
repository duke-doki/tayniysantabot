# Generated by Django 5.0 on 2023-12-13 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santa', '0002_alter_person_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='название окна'),
        ),
        migrations.AlterField(
            model_name='party',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='название группы'),
        ),
    ]