from kivymd.uix.boxlayout import MDBoxLayout

from .base import BaseAuthScreen
from ui.field.input import FDInput
from ui.field.button import FDRectangleButton
from service.server.auth import auth_user
from validators import register as RegisterValidator


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
