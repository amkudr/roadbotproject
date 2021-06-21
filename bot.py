import logging

from handlers import active_trips, greet_user, check_in, name_user , active_trips, create_trip, car_registration, phone 

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from telegram import User
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(MessageHandler(Filters.regex('^(да)$'),car_registration))
    dp.add_handler(MessageHandler(Filters.regex('^(нет)$'), active_trips))
    dp.add_handler(MessageHandler(Filters.regex('^(Создать поездку)$'), create_trip))
    dp.add_handler(MessageHandler(Filters.regex('^(Активные поездки)$'), active_trips))
    dp.add_handler(MessageHandler(Filters.regex('^(Зарегистрироваться)$'), check_in))
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('\d+'), phone))
    dp.add_handler(MessageHandler(Filters.text, name_user))
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()