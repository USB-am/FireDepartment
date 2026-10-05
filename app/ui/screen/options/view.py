from typing import TYPE_CHECKING

from kivymd.uix.dialog import MDDialog

from ui.screen.base import BaseScrollScreen
from ui.screen.utils.decorators import lazy_create
from ui.widgets.user_profile_preview import FDUserProfilePreview
from ui.widgets.drop_down_menu import FDDropDownMenu


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
        self._create_duty_change()

    @lazy_create('user_profile_preview')
    def _create_user_profile_preview(self) -> None:
        self.user_profile_preview = FDUserProfilePreview()

        self.user_profile_preview.set_avatar_image('/home/admin/Downloads/Gemini_Generated_Image_ponzcdponzcdponz.png')
        self.user_profile_preview.set_username('Username')
        self.user_profile_preview.set_sign_call('Kama2')
        self.user_profile_preview.set_part_number('43')

        self.user_profile_preview.add_button(icon='bus', text='Button #1', callback=lambda *_: print('Button #1'))
        self.user_profile_preview.add_button(icon='bus', text='Button #2', callback=lambda *_: print('Button #2'))
        self.user_profile_preview.add_button(icon='cog', text='Settings', callback=lambda *_: self.path_manager.forward('profile'))

        self.add_content(self.user_profile_preview)

    @lazy_create('duty_change')
    def _create_duty_change(self) -> None:
        localize_title = self.lang_manager.get_text('Duty change')
        duty_items = [
            {
                'text': f'Duty #{i}',
                'viewclass': 'OneLineListItem',
                'on_release': lambda *_: print(f'Duty #{i}')
            }
            for i in range(4)
        ]
        self.duty_change = FDDropDownMenu(
            title=localize_title,
            items=duty_items)

        self.add_content(self.duty_change)
