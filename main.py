from telegram.ext import Updater, CommandHandler

from handlers import greet_user, car_registration, trip_registration
import settings


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher

    dp.add_handler(car_registration)
    dp.add_handler(trip_registration)
    dp.add_handler(CommandHandler("start", greet_user))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
