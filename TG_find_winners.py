import os
import datetime
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tayniysantabot.settings')
django.setup()


from santa.models import Party, Message, Person, Winner


def find_winners():
    parties = Party.objects.all()
    if parties.count() > 0:

        for party in parties:

            if (party.end_of_registration.strftime('%Y-%m-%d %H:%M:%S') == datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) and party.winners.count() == 0:
                print('yes!')
                # начинаем жеребьевку
                players = [player.username for player in
                           party.players.all()]
                random.shuffle(players)
                santas = {}
                for username in players:
                    if not username == players[-1]:
                        santas[username] = players[players.index(username) + 1]
                    else:
                        santas[username] = players[0]
                print(santas)
                # теперь у нас есть словарь из кто кому дарит
                for key, value in santas.items():
                    gets_gift = Person.objects.get(username=value)
                    sends_gift = Person.objects.get(username=key)
                    text = (
                            Message.objects.get(name='Победитель').text
                            + '\n'
                            + f'\nИмя: {gets_gift.name}\n'
                            + f'\ntelegram: @{gets_gift.username}\n'
                            + f'\nemail: {gets_gift.email}\n'
                    )

                    # Создаем виннера
                    Winner.objects.create(text=text, santa=sends_gift, party=party)


if __name__ == '__main__':
    while True:
        find_winners()
