from telegram.ext import Updater, CommandHandler

# from actual_trips import actual_trips
from handlers import (
            greet_user, user_registration,
            car_registration, trip_registration)
import settings


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher

    dp.add_handler(user_registration)
    dp.add_handler(car_registration)
    dp.add_handler(trip_registration)
    dp.add_handler(CommandHandler("start", greet_user))
    # dp.add_handler(MessageHandler(Filters.regex("^(Актуальные поездки)$"), actual_trips))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
