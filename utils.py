from telegram import ReplyKeyboardMarkup


def main_keyboard():
    keyboard = ReplyKeyboardMarkup(
            [['Актуальные поездки'], ['Создать поездку']],
            resize_keyboard=True, one_time_keyboard=True)
    return keyboard
