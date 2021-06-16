

import utils

def greet_user(update,context):
    print("Пользователь найден")
    update.message.reply_text('Привет!')
