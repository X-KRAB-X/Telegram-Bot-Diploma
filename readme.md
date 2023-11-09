# Лой

Учебный бот, способный работать с API сторонних сайтов.

## Установка
Помимо клонирования репозитория, нужно установить несколько библиотек:
+ pyTelegramBotAPI
+ python-dotenv
+ peewee


## Использование
Бот работает со следующим списком команд:
+ /start - Бот приветствует  пользователя
+ /help - Бот выводит список своих команд
+ /low - Бот выводит товары по возрастанию цены
+ /high - Бот выводит товары по убыванию цены
+ /custom - Бот выводит товары в указанном диапазоне цены, в случайном порядке
+ /history - Бот выводит пользователю историю его запросов

Вся история запросов сохраняется в базе данных. Она создается автоматически после запуска бота.