import os

import django

import logging
from time import sleep

from environs import Env
from telegram.ext import MessageHandler, Updater, Filters, ConversationHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tayniysantabot.settings')
django.setup()

from santa.models import Party, Answer, Person, Message, Winner

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

ASK_NAME, ASK_EMAIL, WISHLIST, LETTER = range(4)


def intro(update, context):
    print(update.message.text)
    print(type(update.message.text) is int)
    if update.message.text.isdigit():
        print('YA')
        group_id = update.message.text
        group_here = Party.objects.get(id=group_id)
        context.user_data['group_id'] = group_id
        username = update.message.from_user.username
        chat_id = update.message.chat_id
        context.user_data['username'] = username
        player, is_found = Person.objects.get_or_create(username=username,
                                                        chat_id=chat_id)
        player.is_player = True
        player.save()
        group_here.players.add(player)

        intro_text = (
                Message.objects.get(name='Интро игроку').text
                + '\n'
                + f"\nназвание: {group_here.name}\n"
                + f"\nограничение стоимости подарка: {group_here.cost_limit}\n"
                + f"\nпериод регистрации: {group_here.end_of_registration}\n"
                + f"\nдата отправки подарков: {group_here.gift_sending}\n"
        )
        update.message.reply_text(
            intro_text
        )
        sleep(2)

        update.message.reply_text(
            Message.objects.get(name='Запрос имени').text
        )
        return ASK_NAME
    else:
        print(update.message.text)
        player_name = update.message.text
        context.user_data['username'] = update.message.from_user.username
        player = Person.objects.get(username=context.user_data['username'])
        context.user_data['group_id'] = group_id_here
        player.name = player_name
        player.save()
        update.message.reply_text(
            Message.objects.get(name='Запрос адреса').text
        )
        return ASK_EMAIL


def ask_name(update, context):
    player_name = update.message.text
    player = Person.objects.get(username=context.user_data['username'])
    player.name = player_name
    player.save()

    update.message.reply_text(
        Message.objects.get(name='Запрос адреса').text
    )
    return ASK_EMAIL


def ask_email(update, context):
    player_email = update.message.text
    player = Person.objects.get(username=context.user_data['username'])
    player.email = player_email
    player.save()

    update.message.reply_text(
        Message.objects.get(name='Вишлист').text
    )
    return WISHLIST


def wishlist(update, context):
    wishlist = update.message.text
    wishlist = Answer.objects.create(text=wishlist)
    wishlist.message = Message.objects.get(name='Вишлист')

    player = Person.objects.get(username=context.user_data['username'])
    group_here = Party.objects.get(id=context.user_data['group_id'])
    wishlist.person = player
    wishlist.party = group_here
    wishlist.save()

    update.message.reply_text(
        Message.objects.get(name='Письмо санте').text
    )
    return LETTER


def letter(update, context):
    letter_to_santa = update.message.text
    letter_to_santa = Answer.objects.create(text=letter_to_santa)
    letter_to_santa.message = Message.objects.get(name='Вишлист')

    player = Person.objects.get(username=context.user_data['username'])
    group_here = Party.objects.get(id=context.user_data['group_id'])
    letter_to_santa.person = player
    letter_to_santa.party = group_here
    letter_to_santa.save()

    text = (
            Message.objects.get(name='Подтверждение регистрации игрока').text
            + '\n'
            + f'\nДень: {group_here.end_of_registration}\n'
            + f'\nА в это число дарим подарки: {group_here.gift_sending}\n'
    )
    update.message.reply_text(
        text
    )

    return ConversationHandler.END


def fallback(update, context):
    update.message.reply_text(
        'Извините, я вас не понял'
    )


def register_in_group(updater, group_id_yes=''):
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r'^\d+|\w+'), intro)],
        states={
            ASK_NAME: [
                MessageHandler(Filters.text & ~Filters.command, ask_name),
            ],
            ASK_EMAIL: [
                MessageHandler(Filters.text & ~Filters.command, ask_email),
            ],
            WISHLIST: [
                MessageHandler(Filters.text & ~Filters.command, wishlist),
            ],
            LETTER: [
                MessageHandler(Filters.text & ~Filters.command, letter),
            ],
        },
        fallbacks=[MessageHandler(Filters.all, fallback)]
    )
    global group_id_here
    group_id_here = group_id_yes
    updater.dispatcher.add_handler(conv_handler)
