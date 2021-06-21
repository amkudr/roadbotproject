from telegram import ReplyKeyboardMarkup



def greet_user(update, context):
    print('Вызван \start')
    my_keyboard = ReplyKeyboardMarkup([
        ['Создать поездку', 'Активные поездки'],
        ['Зарегистрироваться']
        ],resize_keyboard=True)
    update.message.reply_text(
        f"Здравствуйте, я помогу Вам подобрать попутчиков,\n нажмите одну из кнопок !",
        reply_markup=my_keyboard
    )

def check_in(update, context):
    update.message.reply_text(f'введите: имя')
    

def name_user(update, context):
    user_name = update.message.text 
    print(user_name)
    update.message.reply_text(f'Ваше имя: {user_name}\nвведите номер телефона') 

def phone(update, context):
    user_phone = update.message.text
    update.message.reply_text(f'Ваш номер телефона {user_phone} \n вы зарегистрированы') 


def create_trip(update, context):
    my_keyboard = ReplyKeyboardMarkup([['да', 'нет']], resize_keyboard=True)
    update.message.reply_text(
        f'есть ли у Вас автомобиль?',
        reply_markup=my_keyboard)    

def active_trips(update, context):
    update.message.reply_text (
        f'поездка 1, поездка 2, поездка 3, ....'
        )        

def car_registration(update, context):
    update.message.reply_text(f'укажите данные автомобиля:\nгод выпуска, модель')

def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)