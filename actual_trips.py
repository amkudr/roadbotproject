from telegram import ParseMode
from datetime import datetime

from models import Trip


def actual_trips(update, context):
    request = Trip.query.filter(Trip.date > datetime.today()).all()
    user_text = "<b>Актуальные поездки:</b>"
    i = 1
    for trip in request:
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
        i += 1
    update.message.reply_text(user_text, parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    actual_trips()
