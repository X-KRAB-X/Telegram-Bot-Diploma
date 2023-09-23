""" Файл, содержащий функционал, пока что будущих, команд. """

import telebot
from config import BOT_TOKEN
from states import LoyStates, state_storage
from api import *
from history import save_req

my_bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)
curr_state = 0


@my_bot.message_handler(state=LoyStates.info)
def category(message):
    """
    Функция для выбора категории поиска.
    Создает в хранилище вариант запроса для сайта.
    Затем переключает на состояние, соответсвующее введенной команде.
    """

    if message.text.lower() == 'электроника':

        with my_bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = 'category/electronics'

    elif message.text.lower() == 'мужская одежда':
        with my_bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = "category/men's clothing"

    elif message.text.lower() == 'женская одежда':
        with my_bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = "category/women's clothing"

    elif message.text.lower() == 'ювелирные украшения':
        with my_bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = "category/jewelery"

    elif message.text.lower() != 'все':
        my_bot.send_message(message.from_user.id, 'Не понял.')
        return

    else:
        with my_bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = ''

    my_bot.send_message(message.from_user.id, 'Введите кол-во товара для вывода')

    global curr_state
    my_bot.set_state(message.from_user.id, curr_state, message.chat.id)


@my_bot.message_handler(state='*', commands=['start'])
def start_bot(message):
    """ Простое приветствие. """
    my_bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')


@my_bot.message_handler(state='*', commands=['low'])
def low(message):
    """
    Функция /low
    Служит только для вопроса пользователю и сохранения состояния в глобальной переменной.
    """

    my_bot.send_message(message.chat.id,
                        'В какой категории ищем?\n'
                        'Мужская одежда/Женская одежда/Электроника/Ювелирные украшения/Все'
                        )

    global curr_state
    curr_state = LoyStates.low

    my_bot.set_state(message.from_user.id, LoyStates.info, message.chat.id)


@my_bot.message_handler(state=LoyStates.low)
def low_output(message):
    """
    Основная функция /low
    Использует функцию для получения списка товаров от сайта.
    Затем проверяет введенное кол-во товаров и выводит соответствующее количество.
    В конце сохраняет запрос в базе данных.
    """

    with my_bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        products = send_request(data['req'])
        products = sorted(products, key=lambda dct: dct['price'])

        if int(message.text) > len(products):
            my_bot.send_message(message.from_user.id,
                                f'Введенное кол-во товаров превышает их кол-во на складе ({len(products)}), '
                                f'поэтому вывожу все:')

        for index in range(int(message.text) if int(message.text) <= len(products) else len(products)):
            my_bot.send_message(message.from_user.id,
                                f'Имя товара: {products[index]["title"]}\nЦена: {products[index]["price"]}'
                                )

    save_req('low')

    my_bot.delete_state(message.from_user.id, message.chat.id)
