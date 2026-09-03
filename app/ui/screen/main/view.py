from typing import TYPE_CHECKING

from kivymd.uix.dialog import MDDialog

from ui.screen.base import BaseScrollScreen


if TYPE_CHECKING:
    from utils.path_manager import PathManager
    from .controller import FDMainController


class FDMainScreen(BaseScrollScreen):
    name = 'main'

    def __init__(self, path_manager: 'PathManager'):
        super().__init__(path_manager)

        self.add_left_toolbar_items(icon='menu', callback=self.open_menu)
        self.add_right_toolbar_items(icon='fire-truck', callback=lambda *_: print('Open calls'))

        self.controller: 'FDMainController | None' = None
        self.dialog: MDDialog | None = None
