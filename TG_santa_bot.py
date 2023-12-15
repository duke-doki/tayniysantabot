
import os
import pyinputplus as pyip
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tayniysantabot.settings')
django.setup()

from santa.models import Message
from TG_organizer import create_group
from TG_player import register_in_group

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackContext, CallbackQueryHandler
from environs import Env


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
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
    if option == 'organizer':
        message_text = "Вы Организатор."
        response = create_group(messages)
        if response == 'not allowed':
            # поменять принт на отправку сообщения ботом
            print('У вас нет доступа.')
    elif option == 'player':
        message_text = "Вы Игрок."
        response = register_in_group(messages)
        if response == 'does not exist':
            # поменять принт на отправку сообщения ботом
            print('Такой группы не существует')

    query.edit_message_text(text=message_text)
    update.effective_chat.send_message(text=message_text)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    messages = Message.objects.all()
    telegram_token = env.str('TELEGRAM_TOKEN')

    updater = Updater(token=telegram_token)
    dispatcher = updater.dispatcher

    # обработчик команды /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # обработчик кнопок организатора и игрока
    button_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(button_handler)

    updater.start_polling()

    updater.idle()
