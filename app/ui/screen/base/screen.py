from typing import Callable, cast, TYPE_CHECKING

from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from utils.path_manager import PathManager
from core.config import KV_PATH


if TYPE_CHECKING:
    from service.lang_manager import LangManager
    from main import FDApplication


Builder.load_file(KV_PATH.KV_BASE_SCREEN)


class BScreen(Screen):
    def __init__(self, path_manager: PathManager):
        self.path_manager = path_manager

        current_app = cast('FDApplication', MDApp.get_running_app())
        self.lang_manager: 'LangManager' = current_app.lang_manager
        self.title = self.lang_manager.get_text(self.name)

        super().__init__()

    def add_left_toolbar_items(self, icon: str, callback: Callable) -> None:
        toolbar = self.ids.toolbar
        toolbar.left_action_items.append([icon, lambda x: callback(x)])

    def add_right_toolbar_items(self, icon: str, callback: Callable) -> None:
        toolbar = self.ids.toolbar
        toolbar.right_action_items.append([icon, lambda x: callback(x)])

    def add_content(self, widget: Widget) -> None:
        self.ids.content.add_widget(widget)

    def clear_content(self) -> None:
        self.ids.content.clear_widgets()

    def open_menu(self, *events) -> None:
        self.parent.parent.ids.menu.set_state('open')


class BaseScreen(BScreen):
    pass


class BaseScrollScreen(BScreen):
    pass
