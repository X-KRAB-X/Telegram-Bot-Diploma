""" Файл, содержащий функционал, пока что будущих, команд. """

import telebot
from config import BOT_TOKEN
from states import LoyStates


my_bot = telebot.TeleBot(BOT_TOKEN)


@my_bot.message_handler(commands=['start'])
def start_bot(message):
    """ Простое приветствие. """
    my_bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
