from telegram.ext import (
    ConversationHandler, MessageHandler,
    Filters, CallbackQueryHandler)
import logging

from actual_trips import (
                        actual_trips_show, actual_trips_choice)
from user_registration import (
                        anketa_start, anketa_name,
                        anketa_phone)
from car_registration import (
                        anketa_wrong_answer, car_registration_start,
                        car_registration_model, car_year)
from trip_registration import (
                        trip_registration_start, trip_time,
                        trip_arrival_point, trip_departure_point,
                        inline_handler, trip_car_choice)
from utils import main_keyboard, back_to_main_menu

logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
    update.message.reply_text(
        'Здравствуйте, я бот по поиску попутчиков в путешествиях! С чего начнем?',
        reply_markup=main_keyboard()
    )


user_registration = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(
                '^(Зарегистрироваться)$'), anketa_start)
        ],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "phone": [MessageHandler(Filters.regex('\d+'), anketa_phone)]
        },
        fallbacks=[
            MessageHandler(
                Filters.text | Filters.photo | Filters.video |
                Filters.document | Filters.location, anketa_wrong_answer)
        ]
    )


trip_registration = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(
                '^(Создать поездку)$'), trip_registration_start)
        ],
        states={
            "calendar": [CallbackQueryHandler(inline_handler)],
            "time": [MessageHandler(Filters.regex(
                '^((0|1|2)\d:\d\d)$'), trip_time)],
            "arrival_point": [MessageHandler(
                Filters.text, trip_arrival_point)],
            "departure_point": [MessageHandler(
                Filters.text, trip_departure_point)],
            "car": [
                CallbackQueryHandler(
                    car_registration_start, pattern="new_car"),
                CallbackQueryHandler(trip_car_choice, pattern='\d+')],
            "model": [MessageHandler(Filters.text, car_registration_model)],
            "year": [MessageHandler(Filters.regex(
                '^((2|1)\d\d\d)$'), car_year)]
        },
        fallbacks=[
            CallbackQueryHandler(back_to_main_menu, pattern="back"),
            MessageHandler(
                Filters.text | Filters.photo | Filters.video |
                Filters.document | Filters.location, anketa_wrong_answer)
        ]
    )


actual_trips = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(
                '^(Актуальные поездки)$'), actual_trips_show)
        ],
        states={
            "choice": [
                CallbackQueryHandler(actual_trips_choice, pattern='\d+')]
        },
        fallbacks=[
            CallbackQueryHandler(back_to_main_menu, pattern="back"),
            MessageHandler(
                Filters.text | Filters.photo | Filters.video |
                Filters.document | Filters.location, anketa_wrong_answer)
        ]
    )
