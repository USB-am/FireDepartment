from kivymd.uix.boxlayout import MDBoxLayout

from .base import BaseScreen
from ui.field.input import FDInput, FDNumberInput
from ui.field.button import FDRectangleButton
from service.server.auth import register


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

    def fill_elements(self) -> None:
        ''' Заполнить контент формой регистрации '''

        self._email_field = FDInput(hint_text='E-mail')
        self.add_content(self._email_field)

        self._username_field = FDInput(hint_text='Имя пользователя')
        self.add_content(self._username_field)

        self._password_field = FDInput(hint_text='Пароль')
        self.add_content(self._password_field)

        self._password_reentry_field = FDInput(hint_text='Пароль (повтор)')
        self.add_content(self._password_reentry_field)

        self._fire_department_number = FDNumberInput(hint_text='Номер пожарной станции')
        self.add_content(self._fire_department_number)

        self._submit = FDRectangleButton(title='Зарегестрироваться')
        self._submit.bind_btn(callback=validate_data)
        self.add_content(self._submit)

        self.add_content(MDBoxLayout())
