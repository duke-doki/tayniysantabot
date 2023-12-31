# Generated by Django 5.0 on 2023-12-13 05:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='название окна')),
                ('text', models.TextField(blank=True, null=True, verbose_name='текст окна')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='имя персоны')),
                ('phonenumber', models.CharField(blank=True, max_length=20, null=True, verbose_name='номер персоны')),
                ('email', models.CharField(blank=True, max_length=200, null=True, verbose_name='email персоны')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='адрес персоны')),
                ('chat_id', models.IntegerField(blank=True, null=True, verbose_name='id персоны')),
                ('is_owner', models.BooleanField(blank=True, null=True, verbose_name='Владелец')),
                ('is_organizer', models.BooleanField(blank=True, null=True, verbose_name='Организатор')),
                ('is_player', models.BooleanField(blank=True, null=True, verbose_name='Игрок')),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='название группы')),
                ('cost_limit', models.CharField(blank=True, max_length=200, null=True, verbose_name='лимит стоимости')),
                ('end_of_registration', models.DateTimeField(blank=True, null=True, verbose_name='дата и время окончания регистрации')),
                ('gift_sending', models.DateTimeField(blank=True, null=True, verbose_name='дата отправки подарка')),
                ('players', models.ManyToManyField(blank=True, related_name='parties', to='santa.person', verbose_name='игроки группы')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='текст ответа')),
                ('message', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='santa.message', verbose_name='связь с окном')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='santa.person', verbose_name='чей ответ')),
            ],
        ),
    ]
