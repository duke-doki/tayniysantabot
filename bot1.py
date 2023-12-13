# как будет выглядеть общение с ботом

import os
import pyinputplus as pyip
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tayniysantabot.settings')
django.setup()

from santa.models import Message, Party, Person, Answer

messages = Message.objects.all()
# список всех окон, доступ можно брать по имени или id:
# <QuerySet [<Message: Интро организатору>, <Message: Приветствие>,
# <Message: Создание группы>, <Message: Лимит стоимости>,
# <Message: Выбрать стоимость>, <Message: Период регистрации>,
# <Message: Дата отправки>, <Message: Подтверждение создания группы>,
# <Message: Интро игроку>, <Message: Запрос имени>, <Message: Запрос адреса>,
# <Message: Вишлист>, <Message: Письмо санте>,
# <Message: Подтверждение регистрации игрока>, <Message: Победитель>]>


# организатор
def create_group(organizer):

    # окно <Message: Интро организатору>
    print(messages.get(name='Интро организатору').text)
    # выводится 'Сервис для обмена новогодними подарками. (нажмите кнопку старт)'
    pyip.inputStr(
        allowRegexes=['^/start$'],
        blockRegexes=[('.*', 'Invalid input. Please try again.')]
    )

    # окно <Message: Приветствие>
    print(messages.get(name='Приветствие').text)
    # выводится 'Приветственное сообщение: Организуй тайный обмен подарками,
    # запусти праздничное настроение! (здесь кнопка создать игру)'
    pyip.inputStr(
        allowRegexes=['^Создать игру$'],
        blockRegexes=[('.*', 'Invalid input. Please try again.')]
    )

    # окно <Message: Создание группы>
    print(messages.get(name='Создание группы').text)
    # выводится 'Введите название группы (вводим имя группы)'
    group_name_input = pyip.inputStr()
    new_party = Party.objects.create(name=group_name_input)

    # окно <Message: Лимит стоимости>
    print(messages.get(name='Лимит стоимости').text)
    # выводится 'Ограничение стоимости подарка: да/нет? (кнопки да/ нет)'
    cost_limit_answer = pyip.inputYesNo(yesVal='да', noVal='нет')

    if cost_limit_answer == 'да':
        # окно <Message: Выбрать стоимость>
        print(messages.get(name='Выбрать стоимость').text)
        # выводится 'Напишите верхний предел стоимости подарка (здесь кнопки до
        # 500, 500-1000, 1000-2000)'
        cost_limit = pyip.inputNum()
        new_party.cost_limit = cost_limit
    else:
        new_party.cost_limit = None

    # окно <Message: Период регистрации>
    print(messages.get(name='Период регистрации').text)
    # выводится 'Выберите период регистрации участников: (здесь две кнопки:
    # до 25 и до 31)'
    end_of_registration = pyip.inputDatetime(
        prompt='Введите дату и время (например, 01.01.2022 12:00): ',
        formats=['%d.%m.%Y %H:%M']
    )
    new_party.end_of_registration = end_of_registration

    # окно <Message: Дата отправки>
    print(messages.get(name='Дата отправки').text)
    # выводится 'Выберите дату отправки подарка (показываем календарь?)'
    gift_sending = pyip.inputDatetime(
        prompt='Введите дату и время (например, 01.01.2022 12:00): ',
        formats=['%d.%m.%Y %H:%M']
    )
    new_party.gift_sending = gift_sending

    # окно <Message: Подтверждение создания группы>
    print(messages.get(name='Подтверждение создания группы').text)
    # выводится 'Отлично, Тайный Санта уже готовится к раздаче подарков!
    # (Ссылка)'

    # добавим в группу организатора
    new_party.players.add(organizer)

    new_party.save()


# игрок
def register_in_group(player, group):
    group_here = Party.objects.get(name=group)

    # окно <Message: Интро игроку>
    print(messages.get(name='Интро игроку').text)
    # выводится 'Замечательно, ты собираешься участвовать в игре: (вывести
    # на экран данные об игре: название, ограничение стоимости подарка,
    # период регистрации и дата отправки подарков)'
    print(
        f'название: {group_here.name}, '
        f'ограничение стоимости подарка: {group_here.cost_limit}, '
        f'период регистрации: {group_here.end_of_registration}, '
        f'дата отправки подарков: {group_here.gift_sending} '
    )

    # окно <Message: Запрос имени>
    print(messages.get(name='Запрос имени').text)
    # выводится 'Введите имя (инпут)'
    player_name = pyip.inputStr()
    player.name = player_name

    # окно <Message: Запрос адреса>
    print(messages.get(name='Запрос адреса').text)
    # выводится 'Введите свой адрес (инпут)'
    player_address = pyip.inputStr()
    player.address = player_address

    player.save()

    # окно <Message: Вишлист>
    print(messages.get(name='Вишлист').text)
    # выводится 'Напишите, чего бы вы хотели (инпут)'
    wishlist = pyip.inputStr()
    wishlist_answer = Answer.objects.create(text=wishlist)
    wishlist_answer.message = messages.get(name='Вишлист')
    wishlist_answer.person = player

    wishlist_answer.save()

    # окно <Message: Письмо санте>
    print(messages.get(name='Письмо санте').text)
    # выводится 'мини-письмо Санте (инпут)'
    letter_to_santa = pyip.inputStr()
    letter_to_santa = Answer.objects.create(text=letter_to_santa)
    letter_to_santa.message = messages.get(name='Письмо санте')
    letter_to_santa.person = player

    letter_to_santa.save()

    # окно <Message: Подтверждение регистрации игрока>
    print(messages.get(name='Подтверждение регистрации игрока').text)
    # выводится 'Превосходно, ты в игре! 31.12.2021 мы проведем жеребьевку и
    # ты узнаешь имя и контакты своего тайного друга. Ему и нужно будет
    # подарить подарок!'
    group_here.players.add(player)

    # здесь уже нужен функционал с выбором победителя

    # # окно <Message: Победитель>
    # print(messages.get(name='Победитель').text)
    # # выводится 'Жеребьевка в игре “Тайный Санта” проведена! Спешу сообщить
    # # кто тебе выпал (инфа о победителе)'


user_type = pyip.inputChoice(
    ['Organizer', 'Player'],
    prompt='Are you an Organizer or a Player? \n'
)

if user_type == 'Organizer':
    # здесь надо создать персону с галочкой is_organizer=True
    chat_id = pyip.inputNum(
        prompt='Введите свой чат id (бот возьмет автоматически потом) \n'
    )
    organizer = Person.objects.create(chat_id=chat_id, is_organizer=True)
    create_group(organizer)
else:
    # а здесь создаем персону с галочкой is_player=True и потом уже добавляем
    # в нее остальные данные
    chat_id = pyip.inputNum(
        prompt='Введите свой чат id (бот возьмет автоматически потом) \n'
    )
    player, is_found = Person.objects.get_or_create(chat_id=chat_id)
    player.is_player = True
    player.save()
    group = pyip.inputStr(
        prompt='Введите название группы (бот потом по ссылке определит) \n'
    )
    register_in_group(player, group)
