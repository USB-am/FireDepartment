from typing import List

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField

from . import _BaseWidget


class FDChoice(MDTextField, _BaseWidget):
    ''' Текстовое поле с выпадающим списком для выбора '''

    hint_text = StringProperty()
    items = ListProperty()
    validators = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None
        self._update_trigger = Clock.create_trigger(self._update_menu, 0.2)

        self.bind(text=lambda *args: self._update_trigger())

    def _update_menu(self, *args) -> None:
        if self.menu:
            self.menu.dismiss()
            self.menu = None

        text = self.text.strip()

        filtered = [
            suggestion for suggestion in self.items
            if text.lower() in suggestion.lower()
        ]

        if not filtered:
            return

        menu_items = [
            {
                "text": item,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=item: self._select_suggestion(x),
            }
            for item in filtered
        ]

        self.menu = MDDropdownMenu(
            caller=self,
            items=menu_items,
            width_mult=4,
            max_height=Window.height * 0.5,
            position="center",
        )
        self.menu.open()
    
    def _select_suggestion(self, suggestion):
        self.text = suggestion

        if self.menu:
            self.menu.dismiss()
            self.menu = None

    def add_menu_items(self, items: List[str]) -> None:
        self.items.extend(items)

    def update_menu_items(self, items: List[str]) -> None:
        self.items = items

    def get_value(self) -> str:
        return self.text
