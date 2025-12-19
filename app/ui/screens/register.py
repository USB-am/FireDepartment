from kivymd.uix.boxlayout import MDBoxLayout

from .base import BaseScreen
from ui.field.input import FDInput, FDNumberInput
from ui.field.button import FDRectangleButton
from service.server.auth import register
from validators import register as RegisterValidator


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

        self._submit = FDRectangleButton(title='Зарегестрироваться')
        # self._submit.bind_btn(callback=)
        self.add_content(self._submit)

        self.add_content(MDBoxLayout())
