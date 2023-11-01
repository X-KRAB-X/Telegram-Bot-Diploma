""" Файл, содержащий команду /custom. """


from loader import bot
from states.states import LoyStates
from site_api.api import send_request
from datadase.history_saving import save_req


@bot.message_handler(commands=['custom'])
def custom(message):
    bot.send_message(message.from_user.id, 'Введите начальную цену')
    bot.set_state(message.from_user.id, LoyStates.custom_limits_first, message.chat.id)


@bot.message_handler(state=LoyStates.custom_limits_first, func=lambda message: not message.text.startswith('/'))
def custom_limits_first(message):
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Это не похоже на цифру. Введите еще раз')
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['start'] = int(message.text)

    bot.send_message(message.from_user.id, 'Введите конечную цену')

    bot.set_state(message.from_user.id, LoyStates.custom_limits_second, message.chat.id)


@bot.message_handler(state=LoyStates.custom_limits_second, func=lambda message: not message.text.startswith('/'))
def custom_limits_second(message):
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Это не похоже на цифру. Введите еще раз')
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['end'] = int(message.text)

        if data['end'] < data['start']:
            bot.send_message(message.from_user.id, 'Стартовая цена явно больше конечной - меняю местами')
            data['end'], data['start'] = data['start'], data['end']
        bot.send_message(message.from_user.id, f'Стартовая цена:{data["start"]} Конечная цена:{data["end"]}')

    bot.send_message(message.from_user.id, 'Теперь выберите, в какой категории искать:\n'
                                           'Мужская одежда/Женская одежда/Электроника/Ювелирные украшения/Все')

    bot.set_state(message.from_user.id, LoyStates.custom_info, message.chat.id)


@bot.message_handler(state=LoyStates.custom_info, func=lambda message: not message.text.startswith('/'))
def custom_category(message):
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
        bot.send_message(message.from_user.id, 'Не понял. Введите еще раз')
        return

    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['req'] = ''

    bot.send_message(message.from_user.id, 'Введите кол-во товара для вывода')

    bot.set_state(message.from_user.id, LoyStates.custom_output, message.chat.id)


@bot.message_handler(state=LoyStates.custom_output, func=lambda message: not message.text.startswith('/'))
def custom_output(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        products = send_request(data['req'])
        products = list(filter(lambda dct: data['start'] < dct['price'] < data['end'], products))

        if len(products) == 0:
            bot.send_message(message.from_user.id, 'Товары в этом диапазоне цены отсутствуют.')
        elif int(message.text) > len(products):
            bot.send_message(message.from_user.id,
                                f'Введенное кол-во товаров превышает их кол-во на складе ({len(products)}), '
                                f'поэтому вывожу все что есть:')

        for index in range(int(message.text) if int(message.text) <= len(products) else len(products)):
            bot.send_message(message.from_user.id,
                                f'Имя товара: {products[index]["title"]}\nЦена: {products[index]["price"]}')

    save_req('custom')

    bot.delete_state(message.from_user.id, message.chat.id)
