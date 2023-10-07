"""Файл для сохранения команды в базе данных"""

import os
from peewee import SqliteDatabase, Model, CharField


path = os.path.abspath(os.path.join('datadase', 'history.db'))  # работает только из файла main, иначе путь ломается.
db = SqliteDatabase(path)


class Requests(Model):
    command = CharField()

    class Meta:
        database = db


db.create_tables([Requests])


def save_req(command):
    req = Requests(command=command)
    req.save()
