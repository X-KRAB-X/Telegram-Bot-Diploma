"""Файл для отправки запросов на сайт."""

import requests
import json


def send_request(req):
    answer = requests.get(f'https://fakestoreapi.com/products/{req}')
    data = json.loads(answer.text)
    return data
