from typing import TYPE_CHECKING

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

from utils.path_manager import PathManager
from ui.screen.base import BaseScreen
from ui.screen.utils.decorators import lazy_create
from ui.widgets.text_field import FDTextInput, FDPasswordInput
from ui.widgets.button import FDRectangleFillButton
from validators.widgets import EmptyValidator, EmailValidator
from validators.auth_form import AuthFormValidator


if TYPE_CHECKING:
    from .controller import FDAuthController


class FDAuthScreen(BaseScreen):
    name = 'auth'

    def __init__(self, path_manager: PathManager):
        super().__init__(path_manager)

        self.controller: 'FDAuthController | None' = None
        self.dialog: MDDialog | None = None

    def on_pre_enter(self, *args) -> None:
        self._create_email_field()
        self._create_password_fields()
        self._create_submit_button()
        self._create_register_button()
        self._create_space()

    @lazy_create('email_field')
    def _create_email_field(self) -> None:
        self.email_field = FDTextInput(
            hint_text=self.lang_manager.get_text('email'),
            validators=[
                EmptyValidator(error_msg=self.lang_manager.get_text('not_empty')),
                EmailValidator(error_msg=self.lang_manager.get_text('email_failure'))
            ]
        )
        self.add_content(self.email_field)

    @lazy_create('pwd_field')
    def _create_password_fields(self) -> None:
        self.pwd_field = FDPasswordInput(
            hint_text=self.lang_manager.get_text('password'),
            validators=[
                EmptyValidator(error_msg=self.lang_manager.get_text('not_empty')),
            ]
        )
        self.add_content(self.pwd_field)

    @lazy_create('submit_btn')
    def _create_submit_button(self) -> None:
        self.submit_btn = FDRectangleFillButton(
            text=self.lang_manager.get_text('login')
        )
        self.submit_btn.bind(on_release=self._on_submit)
        self.add_content(self.submit_btn)

    @lazy_create('register_btn')
    def _create_register_button(self) -> None:
        self.register_btn = FDRectangleFillButton(
            text=self.lang_manager.get_text('registration')
        )
        self.register_btn.bind(on_release=lambda *_: self.path_manager.forward('register'))
        self.add_content(self.register_btn)

    @lazy_create('space')
    def _create_space(self) -> None:
        self.space = MDBoxLayout()
        self.add_content(self.space)

    def is_valid(self) -> bool:
        fields = {
            'email_field': self.email_field,
            'password_field': self.pwd_field,
        }

        for field in fields.values():
            field.validate()

        form_validator = AuthFormValidator(
            error_msg='Auth form is invalid!',
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
        ok_btn.bind(on_release=lambda *_: self.dialog.dismiss()) # type: ignore

        self.dialog.open()

    def show_loading(self, active: bool) -> None:
        submit_text = self.lang_manager.get_text('sending') if active else self.lang_manager.get_text('login')

        self.submit_btn.text = submit_text
        self.submit_btn.disabled = active
        self.register_btn.disabled = active

    def _on_submit(self, *_) -> None:
        if self.controller is None:
            raise AttributeError('FDAuthScreen hasn\'t controller attribute!')

        if self.is_valid():
            self.controller.handle_submit(
                email=self.email_field.get_value(),
                password=self.pwd_field.get_value()
            )

    def set_controller(self, controller: 'FDAuthController') -> None:
        self.controller = controller
