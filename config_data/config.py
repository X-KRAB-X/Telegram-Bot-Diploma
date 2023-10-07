""" Файл, загружающий токен из файла .env. """
import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEFAULT_COMMANDS = (
    ('start', 'Запуск'),
    ('low', 'Минимальная цена'),
    ('high', 'Наибольшая цена'),
    ('custom', 'Цена в указаных пределах'),
    ('history', 'История запросов'),
    ('help', 'Справка')
)
