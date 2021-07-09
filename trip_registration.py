from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from datetime import datetime

from db import db_session
from models import Trip, Car
import telegramcalendar


def trip_registration_start(update, context):
    update.message.reply_text(
        "Введите дату поездки DD.MM.YYYY",
        reply_markup=telegramcalendar.create_calendar())
    return "calendar"


def inline_handler(update, context):
    bot = update.callback_query.message.bot
    selected, date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        context.user_data["trip"] = {"date": date.strftime("%d/%m/%Y")}
        bot.send_message(
                        chat_id=update.callback_query.from_user.id,
                        text="Введите время отправления HH:MM",
                        reply_markup=ReplyKeyboardRemove())
        return "time"
    return "calendar"


def trip_time(update, context):
    time = update.message.text
    context.user_data["trip"]["time"] = time
    update.message.reply_text("Введите место отправления")
    return "arrival_point"


def trip_arrival_point(update, context):
    arrival_point = update.message.text
    context.user_data["trip"]["arrival_point"] = arrival_point
    update.message.reply_text(
        "Введите место прибытия "
    )
    return "departure_point"


def trip_departure_point(update, context):
    departure_point = update.message.text
    context.user_data["trip"]["departure_point"] = departure_point
    user_text = f"""
    <b>Дата поездки</b>: {context.user_data["trip"]["date"]}
<b>Время отправления</b>: {context.user_data["trip"]["time"]}
<b>Место отправления</b>: {context.user_data["trip"]["arrival_point"]}
<b>Место прибытия</b>: {context.user_data["trip"]["departure_point"]}
<b>Поездка успешно добавлена</b>
    """
    update.message.reply_text(user_text, parse_mode=ParseMode.HTML)
    day, month, year = map(int, context.user_data["trip"]["date"].split('/'))
    hour, minute = map(int, context.user_data["trip"]["time"].split(':'))
    trip = Trip(
        car_id=Car.query.filter(
                Car.driver_id == update.message.from_user['id']).scalar().id,
        date=datetime(year, month, day, hour, minute),
        arrival_point=context.user_data["trip"]["arrival_point"],
        departure_point=context.user_data["trip"]["departure_point"]
    )
    db_session.add(trip)
    db_session.commit()
    return ConversationHandler.END
