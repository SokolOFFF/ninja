from django.core.management.base import BaseCommand
from data.models import User

import telebot
import exchange_parser.config as config

class Command(BaseCommand):

    help = ''

    def handle(self, *args, **kwargs):
        bot = telebot.TeleBot(config.TOKEN_LOGGER)

        users_logining = {}
        is_changing_settings = {}

        users = User.objects.all()
        for user in users:
            users_logining[int(user.telegram_id)] = False
            is_changing_settings[int(user.telegram_id)] = False

        def error(message):
            bot.send_message(message.chat.id, text="unknown command, please, check your input.")

        def not_logged_in(message):
            bot.send_message(message.chat.id, text="dont try fuck me up, go login, bullshit")
            bot.send_message(message.chat.id, text="type /login to login")

        def check_password(message):
            if message.text == config.PASSWORD:
                user = User.objects.get(telegram_id=str(message.chat.id))
                user.is_logged_in = True
                user.save()
                users_logining[message.chat.id] = False
                bot.send_message(message.chat.id,
                                 text="hello, good boy! you are logged in.\ni set to track 15000 RUBs for you with threshold 1%.\nbtw activate @ninjjjjjjjabot for sendings")
            else:
                bot.send_message(message.chat.id, text="wrong password, try again.")

        def change_settings(message):
            try:
                user = User.objects.get(telegram_id=str(message.chat.id))
                money_amount = int(message.text.split(' ')[0])
                threshold = float(message.text.split(' ')[1])
                user.money_amount = money_amount
                user.spread = threshold
                user.save()
                is_changing_settings[message.chat.id] = False
                bot.send_message(message.chat.id, text='settings updated')
            except Exception as e:
                bot.send_message(message.chat.id, text="fuck off, write normal data")


        @bot.message_handler(content_types=['text'], commands=['help'])
        def handle_help(message):
            bot.send_message(message.chat.id, text="you should know everything by your own.")

        @bot.message_handler(content_types=['text'], commands=['login'])
        def handle_login(message):
            if User.objects.get(telegram_id=str(message.chat.id)).is_logged_in == True:
                bot.send_message(message.chat.id, text="you are logged in")
            else:
                users_logining[message.chat.id] = True
                bot.send_message(message.chat.id, text="password?")

        @bot.message_handler(content_types=['text'], commands=['start'])
        def handle_start(message):
            if User.objects.filter(telegram_id=str(message.chat.id)).exists():
                bot.send_message(message.chat.id, text="good to see you again")
            else:
                bot.send_message(message.chat.id, text="sup. write /login to login")
                User.objects.get_or_create(telegram_id=str(message.chat.id))

        @bot.message_handler(content_types=['text'], commands=['status'])
        def handle_status(message):
            if User.objects.get(telegram_id=str(message.chat.id)).is_logged_in:
                if User.objects.get(telegram_id=str(message.chat.id)).is_subscribed:
                    bot.send_message(message.chat.id,
                                     text=f"you are on the track.\nand you are tracking for {User.objects.get(telegram_id=str(message.chat.id)).money_amount} RUB(s) with {User.objects.get(telegram_id=str(message.chat.id)).spread} threshold")
                else:
                    bot.send_message(message.chat.id,
                                     text=f"you are NOT on the track.\nalso you are tracking for {User.objects.get(telegram_id=str(message.chat.id)).money_amount} RUB(s) with {User.objects.get(telegram_id=str(message.chat.id)).spread} threshold")
            else:
                not_logged_in(message)

        @bot.message_handler(content_types=['text'], commands=['track'])
        def handle_track(message):
            if User.objects.get(telegram_id=str(message.chat.id)).is_logged_in:
                if not User.objects.get(telegram_id=str(message.chat.id)).is_subscribed:
                    bot.send_message(message.chat.id, text="you are on track")
                    user = User.objects.get(telegram_id=str(message.chat.id))
                    user.is_subscribed = True
                    user.save()
                else:
                    bot.send_message(message.chat.id, text="you already tracking")
            else:
                not_logged_in(message)

        @bot.message_handler(content_types=['text'], commands=['untrack'])
        def handle_untrack(message):
            if User.objects.get(telegram_id=str(message.chat.id)).is_logged_in:
                if User.objects.get(telegram_id=str(message.chat.id)).is_subscribed:
                    bot.send_message(message.chat.id, text="pit stop is waiting for you")
                    user = User.objects.get(telegram_id=str(message.chat.id))
                    user.is_subscribed = False
                    user.save()
                else:
                    bot.send_message(message.chat.id, text="you are not subscribed, son")
            else:
                not_logged_in(message)

        @bot.message_handler(content_types=['text'], commands=['settings'])
        def handle_settings(message):
            if User.objects.get(telegram_id=str(message.chat.id)).is_logged_in:
                bot.send_message(message.chat.id,
                                 text="alright, write amount of your money and threshold in percentages (with space between)")
                is_changing_settings[message.chat.id] = True
            else:
                not_logged_in(message)

        @bot.message_handler(content_types=['text'])
        def message_checker(message):
            if message.chat.type == 'private':
                if not users_logining[message.chat.id] and not is_changing_settings[message.chat.id]:
                    error(message)
                else:
                    if users_logining[message.chat.id]:
                        check_password(message)
                    elif is_changing_settings[message.chat.id]:
                        change_settings(message)

        bot.polling(none_stop=True)
