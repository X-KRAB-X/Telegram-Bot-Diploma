""" Файл, содержащий в себе функцию для установки всех команды в бота. """

from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_commands(bot):
    """
    Функция, последовательно загружающая команды в бота.
    """

    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])
