from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import ConversationHandler
from datetime import datetime

from db import db_session
from models import Trip, User


def actual_trips_show(update, context):
    request = Trip.query.filter(Trip.date > datetime.today())\
        .order_by(Trip.date.asc()).all()
    user_text = "<b>Актуальные поездки:</b>"
    i = 0
    context.user_data["trips"] = {}
    user_id = update.message.from_user['id']
    keyboard_list = []
    for trip in request:
        i += 1
        context.user_data["trips"][i] = trip
        time = trip.date.time().strftime('%H:%M')
        date = trip.date.date().strftime('%d/%m/%y')       
        if trip.car.driver_id == user_id:
            is_driver = "<b>(Вы водитель)</b>"
        else:
            is_driver = None
            keyboard_list.append(i)
        user_text += f"""
{i}) <b>{trip.departure_point} - {trip.arrival_point}</b>
      <b>Время:</b> {time} <b>Дата:</b> {date}
      <b>Водитель:</b> {trip.car.driver.name} {is_driver}
      <b>Машина:</b> {trip.car.model}, {trip.car.year} года выпуска
    """    
    check = db_session.query(
        db_session.query(User).filter_by(id=user_id).exists()
        ).scalar()
    if not check:
        context.user_data["from_actual_trips"] = True
        update.message.reply_text(
            user_text,
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(
                    [['Зарегистрироваться']],
                    resize_keyboard=True,
                    one_time_keyboard=True)
                    )
        return ConversationHandler.END
    update.message.reply_text(
        user_text,
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(
        "Для бронирования выберите номер поездки",
        reply_markup=actual_trips_keyboard(keyboard_list)
    )
    return "choice"


def actual_trips_choice(update, context):
    update.callback_query.answer()
    trip_number = int(update.callback_query.data)
    trip = context.user_data["trips"][trip_number]
    user_id = update.callback_query.from_user['id']
    user = User.query.filter(User.id == user_id).first()
    trip.passengers.append(user)
    db_session.commit()
    time = trip.date.time().strftime('%H:%M')
    date = trip.date.date().strftime('%d/%m/%y')
    user_text = f"""
    Вы успешно забронировали место в поездке:

    <b>{trip.departure_point} - {trip.arrival_point}</b>
    <b>Время:</b> {time} <b>Дата:</b> {date}
    <b>Водитель:</b> {trip.car.driver.name}
    <b>Машина:</b> {trip.car.model}, {trip.car.year} года выпуска
    <b>Телефон водителя:</b> {trip.car.driver.phone}
    """
    update.callback_query.edit_message_text(
        text=user_text, parse_mode=ParseMode.HTML, reply_markup=None)
    return ConversationHandler.END


def actual_trips_keyboard(count):
    keyboard = [
        actual_trips_list(count)
    ]
    keyboard.append([InlineKeyboardButton('Назад', callback_data="back")])
    return InlineKeyboardMarkup(keyboard)


def actual_trips_list(keyboard_list):
    trips = []
    for choice in keyboard_list:
        trips.append(InlineKeyboardButton(choice, callback_data=choice))
    return trips


if __name__ == "__main__":
    actual_trips_list()
