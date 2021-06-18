import logging

import utils
logging.basicConfig(filename='bot.log', level=logging.INFO)
 

def greet_user(update, context):
    
    logging.info('User /start')
    update.message.reply_text('Привет!')
