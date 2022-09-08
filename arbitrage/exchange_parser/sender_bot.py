import telebot
import exchange_parser.config as config

from data.models import User

def sendAll(telegram_id, text):
    bot = telebot.TeleBot(config.TOKEN_SENDLER)
    try:
        bot.send_message(telegram_id, text=text)
    except Exception as e:
        print(e, id)

