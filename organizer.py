import os
import pyinputplus as pyip
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tayniysantabot.settings')
django.setup()

from santa.models import Party, Person, AllowedIdentifier


def create_group(messages):
    # сделать так, чтобы username присваивалось значение юзернейма пишущего боту
    username = pyip.inputStr(
        prompt='Введите свой username \n'
    )

    # сверяем с доступными id
    allowed_usernames = [
        allowed.username for allowed in AllowedIdentifier.objects.all()
    ]
    if username not in allowed_usernames:
        return 'not allowed'

    # создаем нового пользователя или берем, если уже создавали
    organizer, is_found = Person.objects.get_or_create(
        username=username, is_organizer=True
    )

    # окно <Message: Интро организатору>
    print(messages.get(name='Интро организатору').text)

    # поменять на кнопку /start, которая продолжит взаимодействие. Если введено
    # что-то другое, бот будет ждать пока не введут /start
    pyip.inputStr(
        allowRegexes=['^/start$'],
        blockRegexes=[('.*', 'Invalid input. Please try again.')]
    )


    # окно <Message: Приветствие>
    print(messages.get(name='Приветствие').text)

    # поменять на кнопку "Создать игру", которая продолжит взаимодействие. Если введено
    # что-то другое, бот будет ждать пока не введут "Создать игру"
    pyip.inputStr(
        allowRegexes=['^Создать игру$'],
        blockRegexes=[('.*', 'Invalid input. Please try again.')]
    )

    # окно <Message: Создание группы>
    print(messages.get(name='Создание группы').text)

    # поменять так, чтобы бот принимал написанное юзером и присваивал это
    # group_name_input
    group_name_input = pyip.inputStr()
    new_party = Party.objects.create(name=group_name_input)

    # Поменять так, чтобы это отправил бот
    print(f'Вот как получить доступ к этой группе: Санты {new_party.id}')

    # окно <Message: Лимит стоимости>
    print(messages.get(name='Лимит стоимости').text)

    # поменять так, чтобы бот принимал написанное юзером и присваивал это
    # cost_limit_answer
    cost_limit_answer = pyip.inputYesNo(yesVal='да', noVal='нет')

    if cost_limit_answer == 'да':
        # окно <Message: Выбрать стоимость>
        print(messages.get(name='Выбрать стоимость').text)

        # поменять так, чтобы бот принимал написанное юзером и присваивал это
        # cost_limit
        cost_limit = pyip.inputNum()
        new_party.cost_limit = cost_limit
    else:
        new_party.cost_limit = None

    # окно <Message: Период регистрации>
    print(messages.get(name='Период регистрации').text)

    # Поменять так, чтобы бот принимал значение типа даты (например, 01.01.2022 12:00)
    # и присваивал end_of_registration
    end_of_registration = pyip.inputDatetime(
        prompt='Введите дату и время (например, 01.01.2022 12:00): ',
        formats=['%d.%m.%Y %H:%M']
    )
    new_party.end_of_registration = end_of_registration

    # окно <Message: Дата отправки>
    print(messages.get(name='Дата отправки').text)

    # Поменять так, чтобы бот принимал значение типа даты (например, 01.01.2022 12:00)
    # и присваивал gift_sending
    gift_sending = pyip.inputDatetime(
        prompt='Введите дату и время (например, 01.01.2022 12:00): ',
        formats=['%d.%m.%Y %H:%M']
    )
    new_party.gift_sending = gift_sending

    # окно <Message: Подтверждение создания группы>
    print(messages.get(name='Подтверждение создания группы').text)

    # добавим в группу организатора
    new_party.players.add(organizer)
    new_party.save()

    return True
