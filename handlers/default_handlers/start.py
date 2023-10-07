from loader import bot

@bot.message_handler(commands=['start'])
def start_bot(message):
    """ Простое приветствие. """
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
