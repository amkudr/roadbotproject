from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ReplyKeyboardRemove, replymarkup
from datetime import datetime

from models import Trip


def actual_trips_show(update, context):
    request = Trip.query.filter(Trip.date > datetime.today()).all()
    user_text = "<b>Актуальные поездки:</b>"
    i = 0
    for trip in request:
        i += 1
        departure_point = trip.departure_point
        arrival_point = trip.arrival_point
        time = trip.date.time().strftime('%H:%M')
        date = trip.date.date().strftime('%d/%m/%y')
        driver_name = trip.car.driver.name
        driver_phone = trip.car.driver.phone
        car_model = trip.car.model
        car_year = trip.car.year
        user_text += f"""
{i}) <b>{departure_point} - {arrival_point}</b>
     <b>Время:</b> {time} <b>Дата:</b> {date}
     <b>Водитель:</b> {driver_name}
     <b>Машина:</b> {car_model}, {car_year} года выпуска
     <b>Телефон водителя:</b> {driver_phone}
    """
    update.message.reply_text(user_text, parse_mode=ParseMode.HTML)
    update.message.reply_text(
        "Выберите номер поездки",
        reply_markup=actual_trips_keyboard(i)
    )
    return "choice"


def actual_trips_choice(update, context):
    update.callback_query.answer()
    choice = update.callback_query.data
    text = f"Вы забронироли место в поездке номер {choice}"
    update.callback_query.edit_message_caption(caption=text)


def actual_trips_keyboard(count):
    keyboard = [
        actual_trips_list(count)
    ]
    return InlineKeyboardMarkup(keyboard)


def actual_trips_list(number):
    list = []
    for choise in range(1, number+1):
        list.append(InlineKeyboardButton(choise, callback_data=choise))
    return list


if __name__ == "__main__":
    actual_trips_list()
