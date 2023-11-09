""" Файл, содержащий команду /history """

from loader import bot
from datadase.history_saving import last_ten, save_req


@bot.message_handler(commands=['history'])
def history_watch(message):
    """
    Функция /history
    Получает последние 10 запросов пользователя из базы данных.
    Затем по очереди выводит их на экран.
    В случае, если пользователь не вводил команд, сообщает ему об этом.
    """

    requests_list = last_ten(message.from_user.id)
    if len(requests_list) == 0:
        bot.send_message(message.from_user.id, 'История запросов пуста.')
        save_req('history', message.from_user.id, 'Была получена история ваших запросов.')
        return

    bot.send_message(message.from_user.id, 'Вот ваши последние запросы:')

    count = 0
    for string in requests_list:
        count += 1
        bot.send_message(message.from_user.id, f'{count}) /{string.command} - {string.info}')

    save_req('history', message.from_user.id, 'Была получена история ваших запросов.')
