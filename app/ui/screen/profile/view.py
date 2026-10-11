from typing import TYPE_CHECKING

from kivymd.uix.dialog import MDDialog

from ui.screen.base import BaseScrollScreen
from ui.screen.utils.decorators import lazy_create
from ui.widgets.button import FDRectangleFillButton
from ui.widgets.text_field import FDTextInput
from service.requests.storage import AppStorage


if TYPE_CHECKING:
    from utils.path_manager import PathManager
    from .controller import FDProfileController
    from service.requests.storage import UserProfile


class FDProfileScreen(BaseScrollScreen):
    name = 'profile'

    def __init__(self, path_manager: 'PathManager'):
        super().__init__(path_manager)

        self.add_left_toolbar_items(icon='arrow-left', callback=lambda _: self.path_manager.back())

        self.user_profile = AppStorage().get_profile()
        if self.user_profile is None:
            raise AttributeError('Not found user profile!')

        self.controller: 'FDProfileController | None' = None
        self.dialog: MDDialog | None = None

    def on_pre_enter(self, *args) -> None:
        self._create_username_change_field()
        self._create_email_change_field()
        self._create_quit_btn()

    @lazy_create('username_change_field')
    def _create_username_change_field(self) -> None:
        username = self.user_profile.username # type: ignore

        self.username_change_field = FDTextInput(
            hint_text=self.lang_manager.get_text('username')
        )
        self.username_change_field.set_value(username if username is not None else '')
        self.add_content(self.username_change_field)

    @lazy_create('email_change_field')
    def _create_email_change_field(self) -> None:
        email = self.user_profile.email #  type: ignore

        self.email_change_field = FDTextInput(
            hint_text=self.lang_manager.get_text('email')
        )
        self.email_change_field.set_value(email if email is not None else '')
        self.add_content(self.email_change_field)

    @lazy_create('quit_button')
    def _create_quit_btn(self) -> None:
        self.quit_button = FDRectangleFillButton(
            text=self.lang_manager.get_text('Quit')
        )
        self.quit_button.md_bg_color = (1, .2, .2, 1)

        self.add_content(self.quit_button)
