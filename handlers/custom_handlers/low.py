""" Файл, содержащий команду /low. """


from loader import bot
from states.states import LoyStates
from site_api.api import send_request
from datadase.history import save_req


@bot.message_handler(commands=['low'])
def low(message):
    """
    Начальная функция /low
    """

    bot.send_message(message.chat.id,
                        'В какой категории ищем?\n'
                        'Мужская одежда/Женская одежда/Электроника/Ювелирные украшения/Все'
                        )

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['curr_comm'] = 'low'

    bot.set_state(message.from_user.id, LoyStates.info, message.chat.id)


@bot.message_handler(state=LoyStates.info, func=lambda message: not message.text.startswith('/'))
def category(message):
    """
    Функция для выбора категории поиска.
    Создает в хранилище вариант запроса для сайта.
    Затем переключает на состояние, соответсвующее введенной команде.
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

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['curr_comm'] == 'low':
            bot.set_state(message.from_user.id, LoyStates.low, message.chat.id)
        elif data['curr_comm'] == 'high':
            bot.set_state(message.from_user.id, LoyStates.high, message.chat.id)


@bot.message_handler(state=LoyStates.low, func=lambda message: not message.text.startswith('/'))
def low_output(message):
    """
    Основная функция /low
    Использует функцию для получения списка товаров от сайта.
    Затем проверяет введенное кол-во товаров и выводит соответствующее количество.
    В конце сохраняет запрос в базе данных.
    """

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        products = send_request(data['req'])
        products = sorted(products, key=lambda dct: dct['price'])

        if int(message.text) > len(products):
            bot.send_message(message.from_user.id,
                                f'Введенное кол-во товаров превышает их кол-во на складе ({len(products)}), '
                                f'поэтому вывожу все:')

        for index in range(int(message.text) if int(message.text) <= len(products) else len(products)):
            bot.send_message(message.from_user.id,
                                f'Имя товара: {products[index]["title"]}\nЦена: {products[index]["price"]}'
                                )

    save_req('low')

    bot.delete_state(message.from_user.id, message.chat.id)