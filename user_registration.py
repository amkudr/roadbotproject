from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from db import db_session
from models import User


def anketa_start(update, context):
    update.message.reply_text(
        'Введите ваше имя и фамилию',
        reply_markup=ReplyKeyboardRemove()
    )
    return 'name'


def anketa_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text('Пожалуйста, введите и имя и фамилию')
        return 'name'
    context.user_data['user'] = {'name': user_name}
    update.message.reply_text('Введите ваш номер телефона')
    return 'phone'


def anketa_phone(update, context):
    user_phone = update.message.text
    context.user_data['user']['phone'] = user_phone
    user_text = f"""
    <b>Имя</b>: {context.user_data["user"]["name"]}
<b>Номер телефона</b>: {context.user_data["user"]["phone"]}
<b>Успешно зарегистрировался</b>
    """
    update.message.reply_text(user_text, parse_mode=ParseMode.HTML)
    user = User(
        id=update.message.from_user['id'],
        name=context.user_data['user']['name'],
        phone=context.user_data['user']['phone']
    )
    db_session.add(user)
    db_session.commit()
    return ConversationHandler.END
