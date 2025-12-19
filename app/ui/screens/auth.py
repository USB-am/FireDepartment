from kivymd.uix.boxlayout import MDBoxLayout

from .base import BaseScreen
from ui.field.input import FDInput
from ui.field.button import FDRectangleButton
from service.server.auth import auth_user


class AuthScreen(BaseScreen):
    ''' Страница авторизации '''

    name = 'auth'
    toolbar_title = 'Авторизация'

    def __init__(self, path_manager: 'PathManager', **options): # type: ignore
        super().__init__(path_manager)
        self.fill_elements()

    def fill_elements(self) -> None:
        ''' Заполнить контент формой авторизации '''
        login_field = FDInput(hint_text='Логин')
        self.add_content(login_field)

        password_field = FDInput(hint_text='Пароль')
        self.add_content(password_field)

        submit = FDRectangleButton(title='Войти')
        submit.bind_btn(callback=lambda: auth_user(login=login_field.get_value(),
                                                   password=password_field.get_value()))
        self.add_content(submit)

        register = FDRectangleButton(title='Регистрация')
        register.bind_btn(callback=lambda: self._path_manager.forward('register'))
        self.add_content(register)

        self.add_content(MDBoxLayout())
