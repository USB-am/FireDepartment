import os
import json

import requests
from requests.exceptions import RequestException

from config import PATH_TO_SERVER


def register(email: str, username: str, pwd: str, fd_number: int) -> requests.Response:
    '''
    Регистрация

    :param login: email создаваемого пользователя
    :param username: отображаемое имя создаваемого пользователя
    :param pwd: пароль создаваемого пользователя
    :param fd_number: номер пожарной станции
    :returns: requests.Response
    '''
    url = os.path.join(PATH_TO_SERVER, 'create-user')
    data = {
        'email': email,
        'username': username,
        'password': pwd,
        'fd_number': fd_number,
    }
    response = requests.post(url, data=json.dumps(data))
    return response


def login(login: str, pwd: str) -> requests.Response:
    '''
    Авторизация

    :param login: email пользователя
    :param pwd: пароль пользователя
    :returns: requests.Response
    '''

    url = os.path.join(PATH_TO_SERVER, 'login')
    data = {
        'email': login,
        'password': pwd
    }
    response = requests.post(url, data=json.dumps(data))
    return response
