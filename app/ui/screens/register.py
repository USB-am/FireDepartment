from typing import Dict, Optional

import requests
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout

from .base import BaseAuthScreen
from ui.field.input import FDInput, FDNumberInput
from ui.field.button import FDRectangleButton
from service.server.auth import register
from service.server.secret_key import SecretKey
from validators import register as RegisterValidator


def send_register_request(form: Dict) -> Optional[requests.Response]:
    ''' Отправить запрос на регистрацию '''
    try:
        response = register(email=form['email'].get_value(),
                            username=form['username'].get_value(),
                            pwd=form['password'].get_value(),
                            fd_number=form['fd_number'].get_value())
        return response
    except requests.exceptions.ConnectionError:
        return None


def save_secret_key(secret_key: str) -> None:
    ''' Сохранить secret_key в файл '''
    secret_key_manager = SecretKey()
    secret_key_manager.value = secret_key


class RegisterScreen(BaseAuthScreen):
    ''' Страница регистрации '''

    name = 'register'
    toolbar_title = 'Регистрация'

    def __init__(self, path_manager: 'PathManager', **options): # type: ignore
        super().__init__(path_manager)

        self.ids.toolbar.add_left_button(
            icon='arrow-left',
            callback=lambda *_: self._path_manager.back()
        )

        self.fill_elements()
        self._form: Dict[str, Widget] = {
            'email': self._email_field,
            'username': self._username_field,
            'password': self._password_field,
            'fd_number': self._fire_department_number
        }

    def fill_elements(self) -> None:
        ''' Заполнить контент формой регистрации '''

        self._email_field = FDInput(hint_text='E-mail')
        self._email_field.validators.extend([
            RegisterValidator.EmptyFieldValidator(
                self._email_field,
                message='Поле не может быть пустым'
            ),
            RegisterValidator.CorrectedEmailValidator(
                email_field=self._email_field,
                message='Email не корректен'
            ),
        ])
        self.add_content(self._email_field)

        self._username_field = FDInput(hint_text='Имя пользователя')
        self._username_field.validators.extend([
            RegisterValidator.EmptyFieldValidator(
                self._username_field,
                message='Поле не может быть пустым'
            ),
        ])
        self.add_content(self._username_field)

        self._password_field = FDInput(hint_text='Пароль')
        self._password_field.validators.extend([
            RegisterValidator.EmptyFieldValidator(
                self._password_field,
                message='Поле не может быть пустым'
            ),
        ])
        self.add_content(self._password_field)

        self._password_reentry_field = FDInput(hint_text='Пароль (повтор)')
        self._password_reentry_field.validators.extend([
            RegisterValidator.EmptyFieldValidator(
                self._password_reentry_field,
                message='Поле не может быть пустым'
            ),
            RegisterValidator.FieldEqualsFieldValidator(
                field_1=self._password_field,
                field_2=self._password_reentry_field,
                message='Пароли должны совпадать'),
        ])
        self.add_content(self._password_reentry_field)

        self._fire_department_number = FDNumberInput(hint_text='Номер пожарной части')
        self._fire_department_number.validators.extend([
            RegisterValidator.EmptyFieldValidator(
                self._fire_department_number,
                message='Поле не может быть пустым'
            ),
        ])
        self.add_content(self._fire_department_number)

        self._submit_btn = FDRectangleButton(title='Зарегестрироваться')
        self._submit_btn.bind_btn(callback=self.submit)
        self.add_content(self._submit_btn)

        self.add_content(MDBoxLayout())

    def is_valid(self) -> bool:
        ''' Валидация формы '''
        form_fields = (self._email_field, self._username_field,
                       self._password_field, self._password_reentry_field,
                       self._fire_department_number)
        return all(map(lambda f: not f.error, form_fields))

    def submit(self) -> None:
        ''' Проверить и отправить форму на сервер '''

        if not self.is_valid():
            self.show_error_message('Для отправки формы необходимо исправить ошибки!')
            return

        res = send_register_request(self._form)
        if res is None:
            self.show_error_message('Не удалось утановить соединение с сервером!')
            return

        if res.status_code == 201:
            secret_key = res.json().get('secret_key')
            save_secret_key(secret_key)
            self.show_info_message('Регистрация прошла успешно!')
            self._path_manager.forward('main')
        else:
            error_detail = res.json().get('detail') if hasattr(res, 'json') \
                else 'Возникла ошибка обработки ответа сервера!'
            error_message = f'[{res.status_code}] {error_detail}'
            self.show_error_message(error_message)
