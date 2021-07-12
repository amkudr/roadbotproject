from telegram import ParseMode
from datetime import datetime

from models import Trip


def actual_trips(update, context):
    request = Trip.query.filter(Trip.date > datetime.today()).all()
    user_text = "<b>Актуальные поездки:</b>"
    i = 1
    for trip in request:
        user_text += f"""
{i}) <b>{trip.departure_point} - {trip.arrival_point}</b>
     <b>Время:</b> {trip.date.time().strftime('%H:%M')} <b>Дата:</b> {trip.date.date().strftime('%d/%m/%y')}
     <b>Водитель:</b> {trip.car.driver.name}
     <b>Машина:</b> {trip.car.model}, {trip.car.year} года выпуска
     <b>Телефон водителя:</b> {trip.car.driver.phone}
    """
        i += 1
    update.message.reply_text(user_text, parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    actual_trips()
