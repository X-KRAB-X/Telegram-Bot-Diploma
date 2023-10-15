""" Главный файл, загружающий бота и команды в него. """

from loader import bot
from utils.set_commands import set_commands
import handlers

if __name__ == '__main__':
    set_commands(bot)
    bot.infinity_polling()
