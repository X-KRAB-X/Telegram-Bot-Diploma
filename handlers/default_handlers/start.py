"""Команда для запуска. Бот здоровается и описывает себя."""

from loader import bot


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                      f'Меня зовут Лой. Я привязанный к складу бот.\n'
                                      f'Чтобы узнать мои команды, напишите /help')
