from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from datetime import date

from db import db_session
from models import Car



def car_registration_start(update, context):
    update.message.reply_text(
        "Введите марку машины и модель",
        reply_markup=ReplyKeyboardRemove()
    )
    return "model"

def car_registration_model(update, context):
    model = update.message.text
    if len(model.split()) < 2:
        update.message.reply_text("Пожалуйста введите марку машины и модель")
        return "model"
    else:
        context.user_data["car"] = {"model": model}
        update.message.reply_text(
            "Введите год выпуска автомобиля"
        )
        return "year_of_issue"

def car_year(update, context):    
    year = int(update.message.text) 
    if year<1920 or year >= date.today().year:
        update.message.reply_text("Пожалуйста введите год выпуска автомобиля")
        return "year_of_issue"
    else:
        context.user_data["car"]["year_of_issue"] = year
        user_text = f"""
        <b>Автомобиль</b>: {context.user_data["car"]["model"]}
<b>Год выпуска</b>: {context.user_data["car"]["year_of_issue"]}
<b>Успешно добавлен</b>
        """
        update.message.reply_text(user_text, parse_mode=ParseMode.HTML)
        car = Car(            
            driver_id = update.message.from_user['id'],        
            model = context.user_data["car"]["model"],
            year_of_issue = context.user_data["car"]["year_of_issue"]               
        ) 
        db_session.add(car)      
        db_session.commit()

        return ConversationHandler.END
        
def anketa_wrong_answer(update, context):
    update.message.reply_text("Неверный запрос")

