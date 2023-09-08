from telebot.handler_backends import State, StatesGroup


class LoyStates(StatesGroup):
    """ Состояния для каждой команды. """

    low = State()
    high = State()
    custom = State()
    history = State()
