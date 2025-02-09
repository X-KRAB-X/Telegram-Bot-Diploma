"""
Файл, содержащий все необходимые состояния.
"""

from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage


state_storage = StateMemoryStorage()


class LoyStates(StatesGroup):

    low_info = State()
    low_output = State()

    high_info = State()
    high_output = State()

    custom_limits_first = State()
    custom_limits_second = State()
    custom_info = State()
    custom_output = State()
