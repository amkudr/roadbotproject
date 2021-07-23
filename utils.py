from telegram import (
    ReplyKeyboardMarkup, InlineKeyboardButton,
    InlineKeyboardMarkup)
from telegram.ext import ConversationHandler

def main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        [['Актуальные поездки'], ['Создать поездку']],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard


def back_to_main_menu(update, context):
    update.callback_query.delete_message()
    update.callback_query.message.reply_text(
        text="Выберите пункт меню",
        reply_markup=main_keyboard())
    return ConversationHandler.END


def back_keyboard():
    keyboard = [
        [InlineKeyboardButton('Назад', callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)
