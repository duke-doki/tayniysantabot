
import os
import pyinputplus as pyip
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tayniysantabot.settings')
django.setup()

from santa.models import Message
from organizer import create_group
from player import register_in_group


if __name__ == '__main__':
    messages = Message.objects.all()

    while True:
        # поменять так, чтобы было 2 кнопки, "Организатор" и "Игрок"
        # и присвоить user_type соответственно 'Organizer' или 'Player'
        # если юзер напишет что то другое, спросить снова
        user_type = pyip.inputChoice(
            ['Organizer', 'Player'],
            prompt='Are you an Organizer or a Player? \n'
        )

        if user_type == 'Organizer':
            response = create_group(messages)
            if response == 'not allowed':
                # поменять принт на отправку сообщения ботом
                print('У вас нет доступа.')
        else:
            response = register_in_group(messages)
            if response == 'does not exist':
                # поменять принт на отправку сообщения ботом
                print('Такой группы не существует')

        # поменять так, чтобы бот спросил попробовать ли снова, если 'да'
        # начать заново, если "нет", закончить сессию до нового /start
        answer = pyip.inputYesNo(
            prompt='Попробуем снова? \n',
            yesVal='да',
            noVal='нет')
        if answer == 'нет':
            break
