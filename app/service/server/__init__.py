import os
from typing import Dict, Optional

import requests
from requests.exceptions import RequestException

from exceptions import NoSecretKeyError


def __get_secret_key() -> Optional[str]:
    ''' Получить secret_key '''
    path_to_secret_key = os.path.join(os.path.dirname(__file__), 'SECRET_KEY')

    if not os.path.exists(path_to_secret_key):
        return None

    with open(path_to_secret_key) as file:
        return file.read()


def add_secret_key_to_headers(headers: Optional[Dict]) -> Dict:
    '''
    Добавить secret_key в headers.

    :param headers: headers для запроса
    :returns: словарь с добавленным secret_key
    '''

    secret_key = __get_secret_key()
    if secret_key is None:
        raise NoSecretKeyError

    if headers:
        headers.update({'secret_key': secret_key})
    else:
        headers = {'secret_key': secret_key}

    return headers


def send_get(url: str, headers: Dict=None) -> requests.Response:
    '''
    Отправить GET запрос на сервер.

    :param url: url на который будет направлен запрос
    :param headers: словарь с дополнительными аргументами
    :returns: requests.Response
    '''

    headers = add_secret_key_to_headers(headers)
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise RequestException
    return res


def send_post(url: str, headers: Dict=None) -> None:
    '''
    Отправить POST запрос на сервер.

    :param url: url на который будет направлен запрос
    :param headers: словарь с дополнительными аргументами
    :returns: None
    '''

    headers = add_secret_key_to_headers(headers)
    res = requests.post(url, headers=headers)
    if res.status_code != 200:
        raise RequestException
