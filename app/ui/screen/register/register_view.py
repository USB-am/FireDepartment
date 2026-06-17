from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout

from ui.screen.based_screen import BaseScreen
from ui.widgets.text_input import FDTextInput, FDPasswordInput
from ui.widgets.button import FDRectangleFillButton
from ui.utils.decorators import lazy_create
from validators.widgets import EmptyValidator, EmailValidator, IdenticalPasswords
from validators.register_form import RegisterFormValidator


class FDRegisterScreen(BaseScreen):
    name = 'register'
    title = 'Регистрация'

    controller = None

    def __init__(self, path_manager: 'PathManager'):
        super().__init__(path_manager)

        self.ids.toolbar.anchor_title = 'center'
        self.add_left_toolbar_items('arrow-left', lambda *_: self.path_manager.back())

        self.dialog = None

    def on_pre_enter(self, *args) -> None:
        self._create_email_field()
        self._create_username_field()
        self._create_password_fields()
        self._create_submit_button()
        self._create_space()

    @lazy_create('email_field')
    def _create_email_field(self) -> None:
        self.email_field = FDTextInput(
            hint_text='Электронная почта',
            validators=[
                EmptyValidator(error_msg='Поле не может быть пустым!'),
                EmailValidator(error_msg='Адрес указан неверно!')
            ]
        )
        self.add_content(self.email_field)

    @lazy_create('username_field')
    def _create_username_field(self) -> None:
        self.username_field = FDTextInput(
            hint_text='Имя пользователя',
            validators=[
                EmptyValidator(error_msg='Поле не может быть пустым!'),
            ]
        )
        self.add_content(self.username_field)

    @lazy_create('pwd_field')
    def _create_password_fields(self) -> None:
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

    @lazy_create('submit_btn')
    def _create_submit_button(self) -> None:
        self.submit_btn = FDRectangleFillButton(
            text='Зарегистрироваться'
        )
        self.submit_btn.bind(on_release=self._on_submit)
        self.add_content(self.submit_btn)

    @lazy_create('space')
    def _create_space(self) -> None:
        self.space = MDBoxLayout()
        self.add_content(self.space)

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

    def open_dialog(self, title: str, message: str) -> None:
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

    def set_controller(self, controller: 'RegisterController') -> None:
        self.controller = controller

    def _on_submit(self, *args) -> None:
        if not self.controller:
            raise AttributeError('FDRegisterScreen hasn\'t controller attribute!')

        if self.is_valid():
            self.controller.handle_submit(
                email=self.email_field.get_value(),
                username=self.username_field.get_value(),
                password=self.pwd_field.get_value()
            )

    def show_loading(self, active: bool) -> None:
        self.submit_btn.text = 'Отправка...' if active else 'Зарегистрироваться'
        self.submit_btn.disabled = active
