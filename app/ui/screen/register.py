from typing import List, Dict

import requests
from kivy.lang.builder import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout

from path_manager import PathManager
from .based_screen import BaseScreen
from ui.widgets.text_input import FDTextInput, FDPasswordInput
from ui.widgets.button import FDRectangleFillButton
from validators.widgets import EmptyValidator, EmailValidator, IdenticalPasswords
from validators.register_form import RegisterFormValidator


class FDRegisterScreen(BaseScreen):
    name = 'register'
    title = 'Регистрация'

    def __init__(self, path_manager: PathManager):
        super().__init__(path_manager)

        self.ids.toolbar.anchor_title = 'center'
        self.add_left_toolbar_items('arrow-left', lambda *_: self.path_manager.back())

        self.form_validator = None
        self.dialog = None

    def on_pre_enter(self, *args) -> None:
        self.clear_content()

        self.email_field = FDTextInput(
            hint_text='Электронная почта',
            validators=[
                EmptyValidator(error_msg='Поле не может быть пустым!'),
                EmailValidator(error_msg='Адрес указан неверно!')
            ]
        )
        self.add_content(self.email_field)

        self.username_field = FDTextInput(
            hint_text='Имя пользователя',
            validators=[
                EmptyValidator(error_msg='Поле не может быть пустым!'),
            ]
        )
        self.add_content(self.username_field)

        self.pwd_field = FDPasswordInput(
            hint_text='Пароль',
            validators=[
                EmptyValidator(error_msg='Поле не может быть пустым!'),
            ]
        )
        self.add_content(self.pwd_field)

        self.pwd_again_field = FDPasswordInput(
            hint_text='Пароль (повтор)',
            validators=[
                EmptyValidator(error_msg='Поле не может быть пустым!'),
                IdenticalPasswords(
                    other_widget=self.pwd_field,
                    error_msg='Пароли не совпадают!')
            ]
        )
        self.add_content(self.pwd_again_field)

        self.submit_btn = FDRectangleFillButton(
            text='Зарегистрироваться'
        )
        self.submit_btn.bind(on_release=self.submit)
        self.add_content(self.submit_btn)

        self.add_content(MDBoxLayout())

        self.test_filled_fields()

    def test_filled_fields(self):
        self.email_field.set_value('qwe@qwe.com')
        self.username_field.set_value('qwe')
        self.pwd_field.set_value('qwe')
        self.pwd_again_field.set_value('qwe')

    def is_valid(self) -> bool:
        fields = {
            'email_field': self.email_field,
            'username_field': self.username_field,
            'password_field': self.pwd_field,
            'password_again_field': self.pwd_again_field,
        }

        for field in fields.values():
            field.validate()

        form_validator = RegisterFormValidator(
            error_msg='Register form is invalid!',
            **fields
        )

        return form_validator.is_valid()

    def open_error_dialog(self, title: str, message: str) -> None:
        if self.dialog is not None:
            self.dialog.dismiss()
            self.dialog = None

        ok_btn = MDFlatButton(text='Ок')

        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[ok_btn,]
        )
        ok_btn.bind(on_release=lambda *_: self.dialog.dismiss())

        self.dialog.open()

    def submit(self, *_) -> None:
        if self.is_valid():
            print(f'Register form is valid')
            self._send_registration()

        else:
            self.open_error_dialog(
                title='Ошибка',
                message='В форма регистрации заполнена неправильно!'
            )

    def _send_registration(self) -> None:
        data = {
            'email': self.email_field.get_value(),
            'username': self.username_field.get_value(),
            'password': self.pwd_field.get_value(),
        }

        response = self.api_client.post(
            endpoint='models/users/register',
            data=data,
            on_success=lambda *_: print('SUCCESS'),
            on_failure=lambda *_: print('FAILURE')
        )

        print(f'{dir(response)=}')

    def __success_register(self, req: 'UrlRequest', result: Dict[str, str]) -> None:
        print(f'SUCCESS [{req.resp_status=}] {result}')

    def __failure_register(self, req: 'UrlRequest', result: Dict[str, str]) -> None:
        print(f'FAILURE [{req.resp_status=}] {result}')
