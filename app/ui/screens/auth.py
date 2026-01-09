from typing import Optional

import requests
from kivymd.uix.boxlayout import MDBoxLayout

from .base import BaseAuthScreen
from ui.field.input import FDInput
from ui.field.button import FDRectangleButton
from service.server.auth import login as LoginUser
from service.server.secret_key import SecretKey
from validators import register as RegisterValidator


def send_login_request(login: str, password: str) -> Optional[requests.Response]:
    '''
    Отправить запрос авторизации на сервер

    :param login: email пользователя
    :param password: пароль пользователя
    :returns requests.Response: {'status_code': 200,
                                 'detail': 'User is login',
                                 'secret_key': <user_secret_key>}
    '''
    try:
        response = LoginUser(login, password)
        return response
    except requests.exceptions.ConnectionError:
        return None


def save_secret_key(secret_key: str) -> None:
    ''' Сохранить secret_key в файл '''
    secret_key_manager = SecretKey()
    secret_key_manager.value = secret_key


class AuthScreen(BaseAuthScreen):
    ''' Страница авторизации '''

    name = 'auth'
    toolbar_title = 'Авторизация'

    def __init__(self, path_manager: 'PathManager', **options): # type: ignore
        super().__init__(path_manager)
        self.fill_elements()

    def fill_elements(self) -> None:
        ''' Заполнить контент формой авторизации '''
        self._login_field = FDInput(hint_text='Логин')
        self._login_field.validators.extend([
           RegisterValidator.EmptyFieldValidator(
                self._login_field,
                message='Поле не может быть пустым'
            ),
        ])
        self.add_content(self._login_field)

        self._password_field = FDInput(hint_text='Пароль')
        self._password_field.validators.extend([
            RegisterValidator.EmptyFieldValidator(
                self._password_field,
                message='Поле не может быть пустым'
            ),
        ])
        self.add_content(self._password_field)

        self._submit_btn = FDRectangleButton(title='Войти')
        self._submit_btn.bind_btn(callback=self.submit)
        self.add_content(self._submit_btn)

        self._register_btn = FDRectangleButton(title='Регистрация')
        self._register_btn.bind_btn(callback=lambda: self._path_manager.forward('register'))
        self.add_content(self._register_btn)

        self.add_content(MDBoxLayout())

    def is_valid(self) -> bool:
        ''' Валидация формы '''
        form_fields = (self._login_field, self._password_field,)
        return all(map(lambda f: not f.error, form_fields))

    def submit(self) -> None:
        ''' Проверить и отправить форму на сервер '''

        if not self.is_valid():
            self.show_error_message('Форма не заполнена!')
            return

        res = send_login_request(
            login=self._login_field.get_value(),
            password=self._password_field.get_value())

        if res is None:
            self.show_error_message('Не удалось утановить соединение с сервером!')
            return

        if res.status_code == 200:
            secret_key = res.json().get('secret_key')
            save_secret_key(secret_key)
            self.show_info_message('Вы авторизировались!')
            self._path_manager.forward('main')
        else:
            error_detail = res.json().get('detail') if hasattr(res, 'json') \
                else 'Возникла ошибка обработки ответа сервера!'
            error_message = f'[{res.status_code}] {error_detail}'
            self.show_error_message(error_message)
