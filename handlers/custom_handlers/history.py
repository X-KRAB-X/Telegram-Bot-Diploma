""" Файл, содержащий команду /history """

from loader import bot
from datadase.history_saving import last_ten, save_req


@bot.message_handler(commands=['history'])
def history_watch(message):
    """
    Функция /history
    Получает последние 10 запросов из базы данных.
    Затем по очереди выводит их на экран.
    В случае пустой базы, сообщает пользователю об этом.
    """

    requests_list = last_ten()
    if len(requests_list) == 0:
        bot.send_message(message.from_user.id, 'История запросов пуста.')
        save_req('history', message.from_user.id)
        return

    bot.send_message(message.from_user.id, 'Вот последние запросы:')

    count = 0
    for comm in requests_list:
        count += 1
        bot.send_message(message.from_user.id, f'{count} - {comm[1]}')

    save_req('history', message.from_user.id)
