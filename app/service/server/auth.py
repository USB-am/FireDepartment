import os

import requests
from requests.exceptions import RequestException

from config import PATH_TO_SERVER


def register(login: str, pwd: str) -> None:
    ''' Регистрация '''


def auth_user(login: str, pwd: str) -> None:
    ''' Авторизация '''
    url = os.path.join(PATH_TO_SERVER, '/create-user')
    res = requests.post(url, headers={
        'username': login,
        'password': pwd
    })

    if res.status_code != 200:
        raise RequestException
