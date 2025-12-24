import os

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
    res = requests.post(url, headers={
    	'email': email,
    	'username': username,
    	'password': pwd,
    	'fd_number': fd_number,
    })
    return res


def auth_user(login: str, pwd: str) -> None:
    ''' Авторизация '''
    url = os.path.join(PATH_TO_SERVER, 'create-user')
    res = requests.post(url, headers={
        'username': login,
        'password': pwd
    })

    if res.status_code != 200:
        raise RequestException
