import telebot

import config
import database

bot = telebot.TeleBot(config.TOKEN_LOGGER)


def check_password(message):
    if message.text == config.PASSWORD:
        database.add_user(message.chat.id)
        bot.send_message(message.chat.id,
                         text="hello, good boy! you are logged in.\ni set to track 15000 RUBs for you with threshold 0%.\nbtw activate @ninjjjjjjjabot for sendings")
        database.isRegistration[message.chat.id] = False
        database.set_money_amount(str(message.chat.id), 15000)
        database.set_threshold(str(message.chat.id), 0)
    else:
        bot.send_message(message.chat.id, text="wrong password, try again.")


def error(message):
    bot.send_message(message.chat.id, text="unknown command, please, check your input.")


def not_logged_in(message):
    bot.send_message(message.chat.id, text="dont try fuck me up, go login, bullshit")
    bot.send_message(message.chat.id, text="type /login to login")


@bot.message_handler(content_types=['text'], commands=['start'])
def handle_start(message):
    if message.chat.id in database.get_users():
        bot.send_message(message.chat.id, text="good to see you again")
    else:
        bot.send_message(message.chat.id, text="sup. write /login to login")
    database.isRegistration[message.chat.id] = False
    database.isSettingAmount[message.chat.id] = False


@bot.message_handler(content_types=['text'], commands=['login'])
def handle_login(message):
    if message.chat.id in database.get_users():
        bot.send_message(message.chat.id, text="you are already logged in.")
    else:
        bot.send_message(message.chat.id, text="enter password:")
        database.isRegistration[message.chat.id] = True


@bot.message_handler(content_types=['text'], commands=['track'])
def handle_track(message):
    if message.chat.id in database.get_users():
        if message.chat.id not in database.get_subscribers():
            bot.send_message(message.chat.id, text="you are on track")
            database.add_subscriber(message.chat.id)
        else:
            bot.send_message(message.chat.id, text="you already tracking")
    else:
        not_logged_in(message)


@bot.message_handler(content_types=['text'], commands=['untrack'])
def handle_untrack(message):
    if message.chat.id in database.get_users():
        if message.chat.id in database.get_subscribers():
            bot.send_message(message.chat.id, text="pit stop is waiting for you")
            database.delete_subscriber(message.chat.id)
        else:
            bot.send_message(message.chat.id, text="you are not subscribed, son")
    else:
        not_logged_in(message)


@bot.message_handler(content_types=['text'], commands=['status'])
def handle_status(message):
    if message.chat.id in database.get_users():
        if message.chat.id in database.get_subscribers():
            bot.send_message(message.chat.id,
                             text=f"you are on the track.\nand you are tracking for {database.get_moneyamount(message.chat.id)} RUB(s) with {database.get_threshold(message.chat.id)} threshold")
        else:
            bot.send_message(message.chat.id,
                             text=f"you are NOT on the track.\nalso you are tracking for {database.get_moneyamount(message.chat.id)} RUB(s) with {database.get_threshold(message.chat.id)} threshold")
    else:
        not_logged_in(message)


@bot.message_handler(content_types=['text'], commands=['settings'])
def handle_settings(message):
    if message.chat.id in database.get_users():
        bot.send_message(message.chat.id,
                         text="alright, write number and threshold in percentages (with space between)")
        database.isSettingAmount[message.chat.id] = True
    else:
        not_logged_in(message)


@bot.message_handler(content_types=['text'], commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, text="you should know everything by your own.")


@bot.message_handler(content_types=['text'])
def messageChecker(message):
    if message.chat.type == 'private':
        if message.chat.id in database.get_users():
            if message.chat.id in database.isSettingAmount:
                try:
                    if database.isSettingAmount[message.chat.id] == True:
                        database.set_money_amount(str(message.chat.id), int(message.text.split(' ')[0]))
                        database.set_threshold(str(message.chat.id), int(message.text.split(' ')[1]))
                        bot.send_message(message.chat.id,
                                         text=f"you set {database.get_moneyamount(message.chat.id)} of RUB(s) to check with threshold {database.get_threshold(message.chat.id)}%")
                        database.isSettingAmount[message.chat.id] = False
                    else:
                        error(message)
                except Exception as e:
                    bot.send_message(message.chat.id, text="fuck off, write normal data")
            else:
                error(message)
        else:
            if message.chat.id in database.isRegistration:
                if database.isRegistration[message.chat.id]:
                    check_password(message)
                else:
                    error(message)
            else:
                not_logged_in(message)


bot.polling(none_stop=True)
