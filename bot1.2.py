from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from uuid import uuid4


game_storage = {}


TITLE, PRICE_LIMIT, PRICE_RANGE, REGISTRATION_PERIOD, CREATE_GAME = range(5)


def start(update: Update, context: CallbackContext) -> int:
    args = context.args
    if args:
        game_id = args[0]
        game_info = game_storage.get(game_id)
        if game_info:
            name = game_info.get('title')
            price_limit = game_info.get('price_range')
            registration_period = game_info.get('registration_period')
            update.message.reply_text(
                f"Замечательно, ты собираешься участвовать в игре:{name},\n"
                f"ограничение стоимости подарка: {price_limit},\n "
                f"период регистрации для участия: {registration_period}."
            )
        else:
            update.message.reply_text("Извините, эта игра не существует или ссылка недействительна")
        return ConversationHandler.END
    else:
        keyboard = [["Создать игру"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text(
            "Организуй тайный обмен подарками, запусти праздничное настроение!",
            reply_markup=reply_markup
        )
        return TITLE
    

def title(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Введите название игры:",
        reply_markup=ReplyKeyboardRemove()
    )
    return PRICE_LIMIT


def price_limit(update: Update, context: CallbackContext) -> int:
    context.user_data['title'] = update.message.text
    keyboard = [["Да", "Нет"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Ограничим стоимость подарка?",
        reply_markup=reply_markup
    )
    return PRICE_RANGE


def price_range(update: Update, context: CallbackContext) -> int:
    if update.message.text == "Да":
        keyboard = [["до 500 рублей", "500-1000 рублей", "1000-2000 рублей"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text(
            "Выберите ценовой диапазон:",
            reply_markup=reply_markup
        )
        return REGISTRATION_PERIOD
    else:
        context.user_data['price_range'] = "Лимит не установлен"
        return registration_period(update, context)


def registration_period(update: Update, context: CallbackContext) -> int:
    keyboard = [["до 25.12.2021 12:00", "до 31.12.2021 12:00"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Выберите период регистрации участников:",
        reply_markup=reply_markup
    )
    return CREATE_GAME


def create_game(update: Update, context: CallbackContext) -> int:
    context.user_data['registration_period'] = update.message.text

    game_id = str(uuid4())
    context.user_data['game_id'] = game_id

    game_storage[game_id] = {
        'title': context.user_data.get('title'),
        'price_range': context.user_data.get('price_range'),
        'registration_period': context.user_data.get('registration_period'),
    }

    update.message.reply_text(
        "Отлично, Тайный Санта уже готовится к раздаче подарков! "
        "Поделитесь этой ссылкой с участниками, чтобы они могли присоединиться:",
        reply_markup=ReplyKeyboardRemove()
    )

    bot_username = 'Secret_santito_bot'  

    invitation_link = f"https://t.me/{bot_username}?start={game_id}"

    update.message.reply_text(invitation_link)

    return ConversationHandler.END


def main() -> None:
    
    TELEGRAM_TOKEN = '6734508688:AAHNZ7fxKlUdMR05n3M_DIMY8Tb5pOss_vI'

    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TITLE: [MessageHandler(Filters.text & ~Filters.command, title)],
            PRICE_LIMIT: [MessageHandler(Filters.text & ~Filters.command, price_limit)],
            PRICE_RANGE: [MessageHandler(Filters.text & ~Filters.command, price_range)],
            REGISTRATION_PERIOD: [MessageHandler(Filters.text & ~Filters.command, registration_period)],
            CREATE_GAME: [MessageHandler(Filters.text & ~Filters.command, create_game)],
        },
        fallbacks=[]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()