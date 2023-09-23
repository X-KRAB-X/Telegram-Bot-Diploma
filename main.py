""" Здесь происходит только запуск бота. """

from handlers import *
from telebot import custom_filters


if __name__ == '__main__':
    my_bot.add_custom_filter(custom_filters.StateFilter(my_bot))
    my_bot.infinity_polling()

# База данных содержит:
# ('Кросовки', 25, 3000)
# ('Кепки', 10, 700)
# ('Шорты', 13, 1600)
# ('Джинсы', 18, 2500)
# ('Футболки', 20, 1000)
# ('Носки', 30, 500)
# ('Толстовки', 16, 2750)
