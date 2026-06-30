from typing import Optional
from dataclasses import dataclass

from ui.screen.based_screen import BaseScrollScreen
from ui.utils.decorators import lazy_create
from ui.layout.profile import FDProfileLayout


@dataclass
class UserProfileData:
    username: str
    email: str
    firedepartment: str
    fd_number: int
    avatar: Optional[str]


class FDOptionsScreen(BaseScrollScreen):
    name = 'options'
    title = 'Настройки'

    controller = None

    def __init__(self, path_manager: 'PathManager'):
        super().__init__(path_manager)

        self.add_left_toolbar_items('menu', self.open_menu)
        self.add_right_toolbar_items('sync-circle', lambda *_: print('reset options'))

    def on_pre_enter(self, *args) -> None:
        self._create_profile_layout()

    @lazy_create('profile_layout')
    def _create_profile_layout(self) -> None:
        self.profile_layout = FDProfileLayout(title='Профиль')
        user_data = UserProfileData(
            username='Test user',
            email='user@user.com',
            firedepartment='МЧС РОССИИ ПО Г. МОСКВА',
            fd_number='73',
            avatar=None)
        self.profile_layout.update(user_data)
        self.add_content(self.profile_layout)

    def set_controller(self, controller: 'OptionsController') -> None:
        self.controller = controller
