import os
import django
from urllib.parse import urlencode, urlunparse
from environs import Env
from telegram import ReplyKeyboardMarkup
from telegram.ext import MessageHandler, Filters, ConversationHandler
import logging
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tayniysantabot.settings')
django.setup()

from santa.models import Party, Person, AllowedIdentifier, Message


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

(GREETING, CREATE_GAME, PRICE_LIMIT, PRICE, PRICE_LIMIT_IF_YES, REGISTRATION_END_DATE,
 GIFT_SENDING_DATE) = range(7)


def intro(update, context):
    # здесь надо чтобы бот сам определил ник пишущего
    username = update.message.from_user.username
    chat_id = update.message.chat_id
    context.user_data['username'] = username
    # сверяем с доступными id
    allowed_usernames = [
        allowed.username for allowed in AllowedIdentifier.objects.all()
    ]

    if username in allowed_usernames:
        # создаем нового пользователя или берем, если уже создавали
        organizer, is_found = Person.objects.get_or_create(
            username=username, chat_id=chat_id, is_organizer=True
        )

        reply_keyboard = [['старт', ]]
        update.message.reply_text(
            Message.objects.get(name='Интро организатору').text,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                resize_keyboard=True
            )
        )
        return GREETING


def greeting(update, context):

    reply_keyboard = [['создать игру', ]]

    update.message.reply_text(
        Message.objects.get(name='Приветствие').text,
        rreply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                resize_keyboard=True
            )
    )
    return CREATE_GAME


def create_game(update, context):
    update.message.reply_text(
        Message.objects.get(name='Создание группы').text
    )
    return PRICE_LIMIT


def price_limit(update, context):
    # тут берем ответ с прошлого шага и создаем группу с таким именем
    context.user_data['group_name'] = update.message.text
    group_name_input = context.user_data['group_name']
    new_party = Party.objects.create(name=group_name_input)
    context.user_data['group_id'] = new_party.id

    # добавим организатора в группу
    organizer = Person.objects.get(
        username=context.user_data['username'],
        is_organizer=True
    )
    new_party.players.add(organizer)
    new_party.save()

    price_limit_text = Message.objects.get(name='Лимит стоимости').text
    update.message.reply_text(
        f'Вот как получить доступ к этой группе: '
        f'{new_party.name} {new_party.id} \n'
        + price_limit_text
    )
    return PRICE


def price(update, context):
    # присваиваем да или нет
    context.user_data['cost_limit_answer'] = update.message.text
    cost_limit_answer = context.user_data['cost_limit_answer']

    # получаем ранее созданную группу
    new_party = Party.objects.get(
        name=context.user_data['group_name'],
        id=int(context.user_data['group_id'])
    )

    if cost_limit_answer == 'да':
        update.message.reply_text(
            Message.objects.get(name='Выбрать стоимость').text
        )
        return PRICE_LIMIT_IF_YES
    elif cost_limit_answer == 'нет':
        new_party.cost_limit = None
        new_party.save()
        update.message.reply_text(
            Message.objects.get(name='Период регистрации').text
        )
        return REGISTRATION_END_DATE


def price_limit_if_yes(update, context):
    new_party = Party.objects.get(
        id=int(context.user_data['group_id'])
    )
    cost_limit = update.message.text
    new_party.cost_limit = cost_limit
    new_party.save()
    update.message.reply_text(
        Message.objects.get(name='Период регистрации').text
    )
    return REGISTRATION_END_DATE


def registration_end_date(update, context):
    context.user_data['registration_end_date'] = update.message.text
    end_of_registration = context.user_data['registration_end_date']
    end_of_registration = datetime.strptime(end_of_registration, '%d.%m.%Y %H:%M')
    new_party = Party.objects.get(
        id=int(context.user_data['group_id'])
    )

    new_party.end_of_registration = end_of_registration
    new_party.save()
    update.message.reply_text(
        Message.objects.get(name='Дата отправки').text
    )
    return GIFT_SENDING_DATE


def create_invitation_link(bot_username, game_id):
    base_url = "t.me"
    path = f"/{bot_username}"
    query_params = {"start": game_id}
    query_string = urlencode(query_params)
    return urlunparse(('https', base_url, path, '', query_string, ''))


def gift_sending_date(update, context):
    context.user_data['gift_sending_date'] = update.message.text
    gift_sending = context.user_data['gift_sending_date']
    gift_sending = datetime.strptime(gift_sending, '%d.%m.%Y %H:%M')
    new_party = Party.objects.get(
        name=context.user_data['group_name'],
        id=int(context.user_data['group_id'])
    )

    new_party.gift_sending = gift_sending
    new_party.save()

    env = Env()
    env.read_env()
    bot_username = env.str('BOT_USERNAME')

    invitation_link = create_invitation_link(bot_username, context.user_data['group_id'])

    confirmation_message_text = Message.objects.get(name='Подтверждение создания группы').text

    full_message = (
        f"{confirmation_message_text}\n"
        f"Поделитесь этой ссылкой с участниками, чтобы они могли присоединиться:\n"
        f"{invitation_link}"
        )

    update.message.reply_text(full_message)

    return ConversationHandler.END


def fallback(update, context):
    update.message.reply_text(
        'Извините, я вас не понял'
    )


def create_group(updater):

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, intro)],
        states={
            GREETING: [
                MessageHandler(Filters.regex('^старт$') & ~Filters.command, greeting),
            ],
            CREATE_GAME: [
                MessageHandler(Filters.regex('^создать игру$') & ~Filters.command, create_game),
            ],
            PRICE_LIMIT: [
                MessageHandler(Filters.text & ~Filters.command, price_limit),
            ],
            PRICE: [
                MessageHandler(Filters.text & ~Filters.command, price),
            ],
            PRICE_LIMIT_IF_YES: [
                MessageHandler(Filters.text & ~Filters.command, price_limit_if_yes),
            ],
            REGISTRATION_END_DATE: [
                # Тут надо пофиксить regex для даты
                MessageHandler(Filters.regex(r'\d{2}.\d{2}.\d{4} \d{2}:\d{2}') & ~Filters.command, registration_end_date),
            ],
            GIFT_SENDING_DATE: [
                MessageHandler(Filters.regex(r'\d{2}.\d{2}.\d{4} \d{2}:\d{2}') & ~Filters.command, gift_sending_date),
            ],
        },
        fallbacks=[MessageHandler(Filters.all, fallback)]
    )

    updater.dispatcher.add_handler(conv_handler)