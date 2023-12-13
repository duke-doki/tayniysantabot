from django.db import models


class Person(models.Model):
    name = models.CharField(
        'имя персоны',
        max_length=200
    )
    phonenumber = models.CharField(
        'номер персоны',
        max_length=20,
        null=True,
        blank=True
    )
    email = models.CharField(
        'email персоны',
        max_length=200,
        null=True,
        blank=True
    )
    address = models.CharField(
        'адрес персоны',
        max_length=100,
        null=True,
        blank=True
    )
    chat_id = models.IntegerField(
        'id персоны',
        null=True,
        blank=True
    )
    is_owner = models.BooleanField(
        'Владелец',
        null=True,
        blank=True
    )
    is_organizer = models.BooleanField(
        'Организатор',
        null=True,
        blank=True
    )
    is_player = models.BooleanField(
        'Игрок',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Party(models.Model):
    name = models.CharField(
        'название группы',
        max_length=200
    )
    players = models.ManyToManyField(
        Person,
        verbose_name='игроки группы',
        blank=True,
        related_name='parties'
    )
    cost_limit = models.CharField(
        'лимит стоимости',
        max_length=200,
        null=True,
        blank=True
    )
    end_of_registration = models.DateTimeField(
        'дата и время окончания регистрации',
        null=True,
        blank=True
    )
    gift_sending = models.DateTimeField(
        'дата отправки подарка',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Message(models.Model):
    name = models.CharField(
        'название окна',
        max_length=200
    )
    text = models.TextField(
        'текст окна',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Answer(models.Model):
    text = models.TextField(
        verbose_name='текст ответа'
    )
    message = models.OneToOneField(
        Message,
        verbose_name='связь с окном',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        Person,
        verbose_name='чей ответ',
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    def __str__(self):
        return f'Ответ {self.pk}'
