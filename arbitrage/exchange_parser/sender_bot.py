import telebot
import exchange_parser.config as config

from data.models import User

def sendAll(text):
    bot = telebot.TeleBot(config.TOKEN_SENDLER)
    subs = User.objects.filter(is_subscribed=True)
    for sub in subs:
        try:
            bot.send_message(sub.telegram_id, text=text)
        except Exception as e:
            print(e, id)
