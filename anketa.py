from handlers import choice
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup

def anketa_start(update, context):
    update.message.reply_text(
        'Введите Ваши имя фамилию',
        reply_markup= ReplyKeyboardRemove()
    )
    return 'name'

def anketa_name(update, context):
    user_name= update.message.text
    my_keyboard = ReplyKeyboardMarkup(
        [['создать поездку', 'выбрать актуальную поездку']], resize_keyboard=True)
    if len(user_name.split()) < 2:
        update.message.reply_text('пожалуйста введите и имя и фамилию')
        return 'name'
    
    else:
        context.user_data['anketa']= {'name': user_name}
        update.message.reply_text('введите номер телефона')
        return 'phone'

def anketa_phone(update, context):
    user_phone= update.message.text

    context.user_data['anketa']= {'phone': user_phone}
    update.message.reply_text('выберите следующее действие')
    #return 'choice'