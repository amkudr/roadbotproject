from telegram.ext import ConversationHandler,MessageHandler, Filters
import logging

from create_user import get_or_create_user
from car_registration import anketa_wrong_answer, car_registration_start, car_registration_model, car_year
from utils import main_keyboard
logging.basicConfig(filename='bot.log', level=logging.INFO)
 

def greet_user(update, context):
    
    logging.info('User /start')
    #get_or_create_user(update) #Файл вместо регистрации. Временный
    update.message.reply_text(
        'Привет!',
        reply_markup = main_keyboard()
    )

car_registration = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Добавить машину)$'), car_registration_start)
        ],
        states={
            "model": [MessageHandler(Filters.text, car_registration_model)],
            "year_of_issue": [MessageHandler(Filters.regex('^((2|1)\d\d\d)$'), car_year)]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, anketa_wrong_answer)
        ]
    )
