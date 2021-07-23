from types import FrameType
from telegram import (
    ParseMode, ReplyKeyboardRemove,
    InlineKeyboardButton, InlineKeyboardMarkup, replymarkup)
from telegram.ext import ConversationHandler
from datetime import datetime

from db import db_session
from models import Trip, Car
import telegramcalendar
from utils import back_to_main_menu, back_keyboard


def trip_registration_start(update, context):

    update.message.reply_text(
        "Выберите дату поездки",
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
            reply_markup=back_keyboard())
        return "time"
    return "calendar"


def trip_time(update, context):
    time = update.message.text
    context.user_data["trip"]["time"] = time
    update.message.reply_text(
        "Введите место отправления",
        reply_markup=back_keyboard())
    return "arrival_point"


def trip_arrival_point(update, context):
    arrival_point = update.message.text
    context.user_data["trip"]["arrival_point"] = arrival_point
    update.message.reply_text(
        "Введите место прибытия",
        reply_markup=back_keyboard()
    )
    return "departure_point"


def trip_departure_point(update, context):
    departure_point = update.message.text
    context.user_data["trip"]["departure_point"] = departure_point
    user_id = update.message.from_user['id']
    update.message.reply_text(
        "Выберите машину",
        reply_markup=cars_keyboard(user_id)
    )
    return "car"


def trip_car_choice(update, context):
    car_id = update.callback_query.data
    user_text = f"""
    <b>Дата поездки</b>: {context.user_data["trip"]["date"]}
<b>Время отправления</b>: {context.user_data["trip"]["time"]}
<b>Место отправления</b>: {context.user_data["trip"]["arrival_point"]}
<b>Место прибытия</b>: {context.user_data["trip"]["departure_point"]}
<b>Поездка успешно добавлена</b>
    """
    update.callback_query.edit_message_text(
        text=user_text, parse_mode=ParseMode.HTML, reply_markup=None)
    day, month, year = map(int, context.user_data["trip"]["date"].split('/'))
    hour, minute = map(int, context.user_data["trip"]["time"].split(':'))
    trip = Trip(
        car_id=car_id,
        date=datetime(year, month, day, hour, minute),
        arrival_point=context.user_data["trip"]["arrival_point"],
        departure_point=context.user_data["trip"]["departure_point"]
    )
    db_session.add(trip)
    db_session.commit()
    return ConversationHandler.END


def cars_keyboard(user_id):
    cars_info = Car.query.filter(Car.driver_id == user_id).all()
    cars = []
    for car in cars_info:
        car_text = f"{car.model} {car.year} года выпуска"
        cars.append([InlineKeyboardButton(car_text, callback_data=car.id)])
    cars.append([InlineKeyboardButton(
        'Добавить машину', callback_data="new_car")])
    cars.append([InlineKeyboardButton('Назад', callback_data="back")])
    keyboard = InlineKeyboardMarkup(cars)
    return keyboard
