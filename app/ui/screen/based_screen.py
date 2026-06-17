from typing import Callable

from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen

from path_manager import PathManager
from config import BASE_SCREEN_KV


Builder.load_file(BASE_SCREEN_KV)


class _Base(Screen):
    def __init__(self, path_manager: PathManager):
        self.path_manager = path_manager
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


class BaseScreen(_Base):
    pass
