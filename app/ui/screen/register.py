from typing import List

import requests
from kivy.lang.builder import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout

from path_manager import PathManager
from .based_screen import BaseScreen
from ui.widgets.text_input import FDTextInput, FDPasswordInput
from ui.widgets.choice import FDChoice
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

        self.fire_department_field = FDChoice(
            hint_text='Номер части',
            validators=[
                EmptyValidator(error_msg='Поле не может быть пустым!'),
            ]
        )
        fire_departments_list = self._get_fire_departments_list()
        self.fire_department_field.update_menu_items(fire_departments_list)
        self.add_content(self.fire_department_field)

        self.submit_btn = FDRectangleFillButton(
            text='Зарегистрироваться'
        )
        self.submit_btn.bind(on_release=self.submit)
        self.add_content(self.submit_btn)

        self.add_content(MDBoxLayout())

    def _get_fire_departments_list(self) -> List[str]:
        has_error = False

        try:
            reponse = self.api_client.request(
                method='GET',
                endpoint='models/firedepartments_list')
            return response.json()

        except requests.HTTPError as err:
            has_error = True
            error_title = 'Ошибка!'
            error_msg = 'Сервер не смог выполнить запрос. Проверьте подключение или повторите попытку позже.'
            error_code = err

        except requests.ConnectionError as err:
            has_error = True
            error_title = 'Ошибка подключения!'
            error_msg = 'Превышено время ожидания. Проверьте подключение или повторите попытку позже.'
            error_code = err

        if has_error:
            ok_btn = MDFlatButton(text='Ок')
            dialog = MDDialog(
                title=error_title,
                text=error_msg + f'\n{error_code}',
                buttons=[ok_btn,])
            ok_btn.bind(on_release=lambda *_: dialog.dismiss())

            dialog.open()

            return []

    def is_valid(self) -> bool:
        form_validator = RegisterFormValidator(
            error_msg='Register form is invalid!',
            email_field=self.email_field,
            username_field=self.username_field,
            password_field=self.pwd_field,
            password_again_field=self.pwd_again_field,
            fire_department_field=self.fire_department_field)

        return form_validator.is_valid()

    def submit(self, *_) -> None:
        if self.is_valid():
            print(f'Register form is valid')
        else:
            print(f'Register form is invalid')
