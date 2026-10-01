from typing import TYPE_CHECKING

from kivymd.uix.dialog import MDDialog

from ui.screen.base import BaseScrollScreen
from ui.screen.utils.decorators import lazy_create
from ui.widgets.user_profile_preview import FDUserProfilePreview


if TYPE_CHECKING:
    from utils.path_manager import PathManager
    from .controller import FDOptionsController


class FDOptionsScreen(BaseScrollScreen):
    name = 'options'

    def __init__(self, path_manager: 'PathManager'):
        super().__init__(path_manager)

        self.add_left_toolbar_items(icon='menu', callback=self.open_menu)

        self.controller: 'FDOptionsController | None' = None
        self.dialog: MDDialog | None = None

    def on_pre_enter(self, *args) -> None:
        self._create_user_profile_preview()

    @lazy_create('user_profile_preview')
    def _create_user_profile_preview(self) -> None:
        self.user_profile_preview = FDUserProfilePreview()

        self.user_profile_preview.set_avatar_image('/home/admin/Downloads/Gemini_Generated_Image_ponzcdponzcdponz.png')
        self.user_profile_preview.set_username('Username')
        self.user_profile_preview.set_sign_call('Kama2')
        self.user_profile_preview.add_button(icon='bus', text='Button #1', callback=lambda *_: print('Button #1'))
        self.user_profile_preview.add_button(icon='menu', text='Button #2', callback=lambda *_: print('Button #2'))
        self.user_profile_preview.add_button(icon='user', text='Button #3', callback=lambda *_: print('Button #3'))

        self.add_content(self.user_profile_preview)
