import logging
from re import RegexFlag

from handlers import active_trips, active_trips, choice, create_trip, car_registration
from anketa import anketa_start, anketa_name, anketa_phone

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram import User
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван \start')
    my_keyboard = ReplyKeyboardMarkup([
        ['Зарегистрироваться'],
        ],resize_keyboard=True
    )
    update.message.reply_text(
        f"Здравствуйте, я помогу Вам подобрать попутчиков,\n нажмите кнопку !",
        reply_markup=my_keyboard
    )


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher

    anketa = ConversationHandler(
        entry_points= [
            MessageHandler(Filters.regex('^(Зарегистрироваться)$'), anketa_start)
        ],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "phone": [MessageHandler(Filters.regex('\d+'), anketa_phone)]
            
        },
        fallbacks= []
    )

    dp.add_handler(anketa)
    dp.add_handler(MessageHandler(Filters.regex('^(да)$'),car_registration))
    dp.add_handler(MessageHandler(Filters.regex('^(нет)$'), active_trips))
    dp.add_handler(MessageHandler(Filters.regex('^(Создать поездку)$'), create_trip))
    dp.add_handler(MessageHandler(Filters.regex('^(выбрать актуальную поездку)$'), active_trips))
    
    dp.add_handler(CommandHandler("start", greet_user))
    
    #dp.add_handler(MessageHandler(Filters.text, name_user))
    

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
