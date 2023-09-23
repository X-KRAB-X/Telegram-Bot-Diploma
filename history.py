"""Файл для сохранения команды в базе данных"""


from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase('history.db')


class Requests(Model):
    command = CharField()

    class Meta:
        database = db


db.create_tables([Requests])


def save_req(command):
    req = Requests(command=command)
    req.save()
