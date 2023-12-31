from django.db import models


class Person(models.Model):
    name = models.CharField(
        'имя персоны',
        max_length=200,
        null=True,
        blank=True
    )
    email = models.CharField(
        'email персоны',
        max_length=200,
        null=True,
        blank=True
    )
    username = models.CharField(
        'username персоны',
        max_length=50,
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
        return self.username


class Party(models.Model):
    name = models.CharField(
        'название группы',
        max_length=200,
        null=True,
        blank=True
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
        max_length=200,
        null=True,
        blank=True
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
    message = models.ForeignKey(
        Message,
        verbose_name='связь с окном',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    person = models.ForeignKey(
        Person,
        verbose_name='чей ответ',
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    party = models.ForeignKey(
        Party,
        verbose_name='В какой игре',
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    def __str__(self):
        return f'Ответ {self.pk}'


class AllowedIdentifier(models.Model):
    username = models.CharField(
        'username пользователя',
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username


class Winner(models.Model):
    text = models.TextField(
        'текст',
        null=True,
        blank=True
    )
    santa = models.ForeignKey(
        Person,
        verbose_name='кому придет это сообщение',
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='winners'
    )
    party = models.ForeignKey(
        Party,
        verbose_name='В какой игре',
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='winners'
    )
