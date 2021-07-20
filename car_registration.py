from telegram import ParseMode, ReplyKeyboardRemove
from datetime import date

from db import db_session
from models import Car
from trip_registration import cars_keyboard


def car_registration_start(update, context):
    update.callback_query.message.reply_text(
        "Введите марку машины и модель",
        reply_markup=ReplyKeyboardRemove()
    )
    return "model"


def car_registration_model(update, context):
    model = update.message.text
    if len(model.split()) < 2:
        update.message.reply_text("Пожалуйста введите марку машины и модель")
        return "model"
    context.user_data["car"] = {"model": model}
    update.message.reply_text(
        "Введите год выпуска автомобиля"
    )
    return "year"


def car_year(update, context):
    year = int(update.message.text)
    if year < 1920 or year > date.today().year:
        update.message.reply_text("Пожалуйста введите год выпуска автомобиля")
        return "year"
    context.user_data["car"]["year"] = year
    user_text = f"""
    <b>Автомобиль</b>: {context.user_data["car"]["model"]}
<b>Год выпуска</b>: {context.user_data["car"]["year"]}
<b>Успешно добавлен</b>
    """
    update.message.reply_text(user_text, parse_mode=ParseMode.HTML)
    user_id = update.message.from_user['id']
    car = Car(
        driver_id=user_id,
        model=context.user_data["car"]["model"],
        year=context.user_data["car"]["year"]
    )
    db_session.add(car)
    db_session.commit()
    update.message.reply_text(
        "Выберите машину",
        reply_markup=cars_keyboard(user_id)
    )
    return "car"


def anketa_wrong_answer(update, context):
    update.message.reply_text("Неверный запрос")
