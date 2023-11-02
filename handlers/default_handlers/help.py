"""Команда для показа всех команд бота."""

from loader import bot
from datadase.history_saving import save_req


@bot.message_handler(commands=['help'])
def help_bot(message):
    """
    Функция /help
    Выводит на экран список команд и их функционал.
    """
    bot.send_message(message.chat.id, 'Я могу:\n'
                                      '/low - Показать товары с ценой по возрастанию.\n'
                                      '/high - Показать товары с ценой по убыванию.\n'
                                      '/custom - Показать товары с ценой в указаных пределах.\n'
                                      '/history - Показать историю 10 последних запросов.\n'
                                      '/help - Показать все команды(была введена только что :>)')
    save_req('help')
