""" Файл для работы с базой данных. """


import os
from peewee import SqliteDatabase, Model, CharField


path = os.path.abspath(os.path.join('datadase', 'history.db'))  # работает только из файла main, иначе путь ломается.
db = SqliteDatabase(path)


class Requests(Model):
    """
    Модель для базы данных.
    Хранит в себе id, команду, id пользователя и инофрмацию об введной команде.
    """

    command = CharField()
    user_id = CharField()
    info = CharField()

    class Meta:
        database = db


db.create_tables([Requests])


def save_req(command, user_id, info):
    """
    Функция для создания записи в базе данных.
    """

    req = Requests(command=command, user_id=user_id, info=info)
    req.save()


def last_ten(user_id):
    """
    Функция для получения 10 последних запросов конкретного пользователя.
    """

    commands = Requests.select().where(Requests.user_id == user_id).execute()
    return commands
