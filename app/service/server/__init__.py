import os
from typing import Dict, Optional

import requests
from requests.exceptions import RequestException

from .secret_key import SecretKey
from config import PATH_TO_SERVER
from exceptions import NoSecretKeyError


def add_secret_key_to_headers(headers: Optional[Dict]) -> Dict:
    '''
    Добавить secret_key в headers.

    :param headers: headers для запроса
    :returns: словарь с добавленным secret_key
    '''

    secret_key = SecretKey().value
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
    url = os.path.join(PATH_TO_SERVER, url)
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise RequestException
    return res


def send_post(url: str, headers: Dict=None) -> requests.Response:
    '''
    Отправить POST запрос на сервер.

    :param url: url на который будет направлен запрос
    :param headers: словарь с дополнительными аргументами
    :returns: requests.Response
    '''

    headers = add_secret_key_to_headers(headers)
    url = os.path.join(PATH_TO_SERVER, url)
    res = requests.post(url, headers=headers)
    if res.status_code != 200:
        raise RequestException
    return res
