from typing import Dict, Optional

import requests
from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout

from .base import BaseScreen
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


def open_dialog(title: str, text: str) -> None:
    '''
    Открыть диалоговое окно.

    :param title: заголовок окна
    :param text: текст с сообщением
    '''
    dialog_btn = MDFlatButton(text='OK')
    dialog = MDDialog(
        title=title,
        text=text,
        buttons=[dialog_btn,]
    )
    dialog_btn.bind(on_release=lambda e: dialog.dismiss())
    dialog.open()


class RegisterScreen(BaseScreen):
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

        self._email_field.set_value('user@gmail.com')
        self._username_field.set_value('user')
        self._password_field.set_value('123')
        self._password_reentry_field.set_value('123')
        self._fire_department_number.set_value('73')

    def is_valid(self) -> bool:
        ''' Проверка валидности формы '''
        form_fields = (self._email_field, self._username_field,
                       self._password_field, self._password_reentry_field,
                       self._fire_department_number)
        return all(map(lambda f: not f.error, form_fields))

    def show_error_message(self, msg: str) -> None:
        '''
        Отобразить всплывающее окно с ошибкой.

        :param msg: строка, которая будет выведена в сообщении об ошибке
        :returns None:
        '''
        open_dialog('Ошибка', msg)

    def show_info_message(self, msg: str) -> None:
        '''
        Отобразить всплывающее окно с информацией.

        :param msg: строка, которая будет выведена в сообщении
        :returns None:
        '''
        open_dialog('Информация', msg)

    def submit(self) -> None:
        ''' Проверить и отправить форму на сервер '''

        if not self.is_valid():
            self.show_error_message(msg='Для отправки формы необходимо исправить ошибки!')
            return

        res = send_register_request(self._form)
        if res is None:
            self.show_error_message(msg='Не удалось утановить соединение с сервером!')
            return

        if res.status_code == 201:
            secret_key = res.json().get('secret_key')
            save_secret_key(secret_key)
            self.show_info_message(msg='Регистрация прошла успешно!')
        else:
            try:
                error_detail = res.json().get('detail')
                error_message = f'[{res.status_code}] {error_detail}'
                self.show_error_message(msg=error_message)
            except:
                self.show_error_message(msg='Возникла ошибка обработки ответа сервера!')
