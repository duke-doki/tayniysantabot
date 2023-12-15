import os
import pyinputplus as pyip
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tayniysantabot.settings')
django.setup()

from santa.models import Party, Answer, Person


def register_in_group(messages):
    # поменять так, чтобы бот принимал написанное юзером и присваивал это
    # group
    group_and_id = pyip.inputStr(
        prompt='Введите название группы \n'
    )
    match = re.match(r'(\w+)\s+(\d+)', group_and_id)
    if match:
        group = match.group(1)
        id = match.group(2)
    else:
        return 'does not exist'
    # проверяем существование группы
    existing_groups = [
        existing.name for existing in Party.objects.all()
    ]
    if group not in existing_groups:
        return 'does not exist'

    group_here = Party.objects.get(name=group, id=id)

    # Поменять так, чтобы бот спросил юзернейм и присвоил username написанное
    username = pyip.inputStr(
        prompt='Введите свой username (бот возьмет автоматически потом) \n'
    )
    player, is_found = Person.objects.get_or_create(username=username)
    player.is_player = True
    player.save()


    # окно <Message: Интро игроку>
    print(messages.get(name='Интро игроку').text)
    # поменять принты на отправку сообщения ботом
    print(
        f'название: {group_here.name}, '
        f'ограничение стоимости подарка: {group_here.cost_limit}, '
        f'период регистрации: {group_here.end_of_registration}, '
        f'дата отправки подарков: {group_here.gift_sending} '
    )

    # окно <Message: Запрос имени>
    print(messages.get(name='Запрос имени').text)
    # поменять так, чтобы написанное присваивалось player_name
    player_name = pyip.inputStr()
    player.name = player_name

    # окно <Message: Запрос адреса>
    print(messages.get(name='Запрос адреса').text)
    # поменять так, чтобы написанное присваивалось player_email
    player_email = pyip.inputStr()
    player.email = player_email

    player.save()

    # окно <Message: Вишлист>
    print(messages.get(name='Вишлист').text)
    # поменять так, чтобы написанное присваивалось wishlist
    wishlist = pyip.inputStr()
    wishlist_answer = Answer.objects.create(text=wishlist)
    wishlist_answer.message = messages.get(name='Вишлист')
    wishlist_answer.person = player
    wishlist_answer.party = group_here

    wishlist_answer.save()

    # окно <Message: Письмо санте>
    print(messages.get(name='Письмо санте').text)
    # поменять так, чтобы написанное присваивалось letter_to_santa
    letter_to_santa = pyip.inputStr()
    letter_to_santa = Answer.objects.create(text=letter_to_santa)
    letter_to_santa.message = messages.get(name='Письмо санте')
    letter_to_santa.person = player
    letter_to_santa.party = group_here

    letter_to_santa.save()

    # окно <Message: Подтверждение регистрации игрока>
    print(messages.get(name='Подтверждение регистрации игрока').text)
    group_here.players.add(player)


def find_winner(messages):
    # окно <Message: Победитель>
    print(messages.get(name='Победитель').text)
    # выводится 'Жеребьевка в игре “Тайный Санта” проведена! Спешу сообщить
    # кто тебе выпал (инфа о победителе)'