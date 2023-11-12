"""Файл для отправки запросов на сайт."""

import requests


def send_request(req):
    """
    Функция, получающая ответ от сайта и возвращающая его в формате json.
    """

    answer = requests.get(f'https://fakestoreapi.com/products/{req}')
    data = answer.json()
    return data
