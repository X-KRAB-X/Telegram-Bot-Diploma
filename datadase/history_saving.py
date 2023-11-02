""" Файл для работы с базой данных. """


import os
from peewee import SqliteDatabase, Model, CharField
import sqlite3


path = os.path.abspath(os.path.join('datadase', 'history.db'))  # работает только из файла main, иначе путь ломается.
db = SqliteDatabase(path)


class Requests(Model):
    """
    Модель для базы данных.
    Хранит в себе id и саму команду.
    """

    command = CharField()

    class Meta:
        database = db


db.create_tables([Requests])


def save_req(command):
    """
    Функция для создания записи в базе данных.
    """

    req = Requests(command=command)
    req.save()


def last_ten():
    """
    Функция для получения списка, состоящего из 10 последних записей.
    """

    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM (SELECT * FROM requests ORDER BY id DESC LIMIT 10) t ORDER BY id')
        return cursor.fetchall()
