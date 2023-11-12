""" Файл, содержащий команду /high. """


from loader import bot
from states.states import LoyStates
from site_api.api import send_request
from datadase.history_saving import save_req
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def category_buttons():
    """
    Функция, создающая кнопки.
    """

    markup = ReplyKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        KeyboardButton('Мужская одежда'),
        KeyboardButton('Женская одежда'),
        KeyboardButton('Электроника'),
        KeyboardButton('Ювелирные украшения'),
        KeyboardButton('Все')
    )
    return markup


@bot.callback_query_handler(func=lambda call: True)
def category_callback(call):
    """
    Функция колбэка.
    При нажатии на кнопку, вводит за пользователя соответствующую категорию.
    """

    if call.data == 'мужская одежда':
        bot.answer_callback_query(call.id, 'Мужская одежда')
    elif call.data == 'женская одежда':
        bot.answer_callback_query(call.id, 'Женская одежда')
    elif call.data == 'электроника':
        bot.answer_callback_query(call.id, 'Электроника')
    elif call.data == 'ювелирные украшения':
        bot.answer_callback_query(call.id, 'Ювелирные украшения')
    elif call.data == 'все':
        bot.answer_callback_query(call.id, 'Все')


@bot.message_handler(commands=['high'])
def high(message):
    """
    Начальная функция /high
    Запрашивает у пользователя категорию для поиска
    """

    bot.send_message(message.chat.id,
                        'В какой категории ищем?\n'
                        '(Выберите кнопку внизу)',
                        reply_markup=category_buttons()
                        )

    bot.set_state(message.from_user.id, LoyStates.high_info, message.chat.id)


@bot.message_handler(state=LoyStates.high_info, func=lambda message: not message.text.startswith('/'))
def category(message):
    """
    Функция для выбора категории поиска.
    Создает в хранилище вариант запроса для сайта.
    Затем запрашивает у пользователя кол-во товаров, которое необходимо вывести.
    """

    if message.text.lower() == 'электроника':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = 'category/electronics'

    elif message.text.lower() == 'мужская одежда':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = "category/men's clothing"

    elif message.text.lower() == 'женская одежда':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = "category/women's clothing"

    elif message.text.lower() == 'ювелирные украшения':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = "category/jewelery"

    elif message.text.lower() != 'все':
        bot.send_message(message.from_user.id, 'Не понял.')
        return

    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = ''

    bot.send_message(message.from_user.id, 'Введите кол-во товара для вывода')

    bot.set_state(message.from_user.id, LoyStates.high_output, message.chat.id)


@bot.message_handler(state=LoyStates.high_output, func=lambda message: not message.text.startswith('/'))
def high_output(message):
    """
    Основная функция /high
    Использует функцию для получения списка товаров от сайта.
    Затем проверяет введенное кол-во товаров и выводит соответствующее количество.
    В конце сохраняет запрос в базе данных.
    """

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        products = send_request(data['req'])
        products = sorted(products, key=lambda dct: dct['price'], reverse=True)

        if int(message.text) > len(products):
            bot.send_message(message.from_user.id,
                                f'Введенное кол-во товаров превышает их кол-во на складе ({len(products)}), '
                                f'поэтому вывожу все:')

        for index in range(int(message.text) if int(message.text) <= len(products) else len(products)):
            bot.send_message(message.from_user.id,
                                f'Имя товара: {products[index]["title"]}\nЦена: {products[index]["price"]}'
                                )

    save_req('high', message.from_user.id, 'Были получены самые дорогие товары.')

    bot.delete_state(message.from_user.id, message.chat.id)
