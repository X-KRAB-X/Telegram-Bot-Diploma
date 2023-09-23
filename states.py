"""
Файл, содержащий все состояния:
info - выбор категории поиска.
low - товары по возрастанию.
high - товары по убыванию.
custom - все товары в пределах указаной цены.
history - показ 10-ти последних команд.
"""

from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage


state_storage = StateMemoryStorage()


class LoyStates(StatesGroup):

    info = State()
    low = State()
    high = State()
    custom = State()
    history = State()
