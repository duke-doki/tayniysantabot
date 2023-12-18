import os

import django
import logging


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tayniysantabot.settings')
django.setup()

from santa.models import Message, Party, Person, Winner, AllowedIdentifier
from TG_organizer import create_group
from TG_player import register_in_group

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackContext, CallbackQueryHandler
from environs import Env

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update, context) -> None:
    text = 'Вы организатор или игрок?'
    keyboard = [
        [
            InlineKeyboardButton("Организатор", callback_data='organizer'),
            InlineKeyboardButton("Игрок", callback_data='player'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, reply_markup=reply_markup)


def button(update, context) -> None:
    query = update.callback_query
    query.answer()

    option = query.data
    chat_id = update.effective_chat.id
    if option == 'organizer':
        username = update.effective_user.username
        allowed_usernames = [
            allowed.username for allowed in AllowedIdentifier.objects.all()
        ]
        if username in allowed_usernames:
            organizer, is_found = Person.objects.get_or_create(
                username=username, chat_id=chat_id, is_organizer=True
            )
            reply_keyboard = [['создать игру', ]]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
            context.bot.send_message(
                chat_id=chat_id,
                text=Message.objects.get(name='Приветствие').text,
                reply_markup=markup
            )
            create_group(updater)
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text='Извините, у вас нет доступа. Попросите доступ у '
                     'владельца и напишите /start',
            )
    elif option == 'player':
        message_text = "Введите id игры"
        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
        )
        register_in_group(updater)

    query.edit_message_text(text='Принято.')


def callback_winner(context: CallbackContext):
    if Winner.objects.count() > 0:
        winners = Winner.objects.all()
        for winner in winners:
            context.bot.send_message(chat_id=winner.santa.chat_id, text=winner.text)
            winner.delete()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    messages = Message.objects.all()
    telegram_token = env.str('TELEGRAM_TOKEN')

    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    job = updater.job_queue
    job_second = job.run_repeating(callback_winner, interval=5, first=5)

    # обработчик команды /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # обработчик кнопок организатора и игрока
    button_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(button_handler)

    updater.start_polling()
    updater.idle()
