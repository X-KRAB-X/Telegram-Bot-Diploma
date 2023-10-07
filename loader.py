from telebot import TeleBot
from config_data.config import BOT_TOKEN
from states.states import state_storage
from telebot import custom_filters


bot = TeleBot(BOT_TOKEN, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))
