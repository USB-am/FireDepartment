from typing import List

from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout


Builder.load_string('''
<FDChoice>:
    size_hint: (1, None)
    height: dp(50)

    MDTextField:
        id: text_field
        hint_text: root.hint_text
        on_text: root.update_filter()
        on_text: root.open_menu()
        on_focus: if not self.focus: root.dismiss_menu()
''')


class FDChoice(MDBoxLayout):
    ''' Текстовое поле с выпадающим списком для выбора '''

    hint_text = StringProperty()
    validators = ListProperty([])

    def on_kv_post(self, instance: 'FDChoice') -> None:
        self.is_open = False
        self.all_menu_items = []

        text_field = self.ids.text_field
        self.menu = MDDropdownMenu(
            caller=text_field,
            items=[],
            width_mult=4
        )
        self.menu.bind(on_dismiss=lambda *_: setattr(self, 'is_open', False))

    def add_menu_items(self, items: List[str]) -> None:
        items_for_extend = [
            {
                'text': item,
                'viewclass': 'OneLineListItem',
                'on_release': lambda i=item: self.menu_callback(item)
            } for item in items
        ]
        self.all_menu_items.extend(items_for_extend)

    def update_menu_items(self, items: List[str]) -> None:
        items_for_update = [
            {
                'text': item,
                'viewclass': 'OneLineListItem',
                'on_release': lambda i=item: self.menu_callback(item)
            } for item in items
        ]
        self.all_menu_items = items_for_update

    def update_filter(self) -> None:
        txt = self.get_value().lower()
        filtered = list(filter(
            lambda item: txt in item['text'].lower(),
            self.all_menu_items
        ))
        self.menu.items = filtered

    def open_menu(self) -> None:
        if self.is_open:
            self.dismiss_menu()

        self.menu.open()
        self.is_open = True

    def dismiss_menu(self) -> None:
        self.menu.dismiss()

    def menu_callback(self, text_item: str) -> None:
        self.ids.text_field.text = text_item
        self.dismiss_menu()

    def get_value(self) -> str:
        return self.ids.text_field.text
