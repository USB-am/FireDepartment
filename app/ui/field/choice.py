from typing import Any, List, Dict, Callable, Optional

from kivy.lang.builder import Builder
from kivy.properties import ListProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout


Builder.load_string('''
<_BaseChoiceField>:
    size_hint: 1, None
    height: dp(50)


<ChoiceSelectField>:
    MDTextField:
        id: txt_field
        hint_text: root.title
        on_focus: root.open_menu()


<ChoiceFilterSelectField>:
    MDTextField:
        id: txt_field
        hint_text: root.title
        on_focus: root.open_menu()
        on_text: root.filter_items()
''')


class _BaseChoiceField(MDBoxLayout):
    validators = ListProperty([])

    def __init__(self, title: str, items: List[Dict[str, Any]], *args, **kwargs):
        self.title = title
        super().__init__(*args, **kwargs)
        self.error = False
        self.is_open = False
        self.all_menu_items = items
        self.menu_items = items.copy()
        self.menu = None
        self._external_callbacks = {}
        self._create_menu()

    def _create_menu(self) -> None:
        if self.menu:
            try:
                if hasattr(self.menu, 'unbind'):
                    self.menu.unbind(on_open=self.on_menu_open, on_dismiss=self.on_menu_dismiss)
                if self.menu.parent:
                    self.menu.parent.remove_widget(self.menu)
                self.menu = None
            except:
                pass

        menu_items_with_callback = []
        for item in self.menu_items:
            item_copy = item.copy()
            original_text = item_copy.get('text', '')

            original_on_release = item_copy.get('on_release')

            def create_callback(text=original_text, original_cb=original_on_release):
                def callback(*args):
                    self.menu_callback(text)
                    if original_cb:
                        original_cb(*args)
                return callback

            item_copy['on_release'] = create_callback()
            menu_items_with_callback.append(item_copy)

        self.menu = MDDropdownMenu(
            caller=self.ids.txt_field,
            items=menu_items_with_callback,
        )
        self.menu.bind(on_open=self.on_menu_open, on_dismiss=self.on_menu_dismiss)

    def on_menu_open(self, *_) -> None:
        self.is_open = True

    def on_menu_dismiss(self, *_) -> None:
        self.is_open = False

    def add_menu_items(self, items: List[Dict[str, Any]]) -> None:
        self.all_menu_items.extend(items)
        self.menu_items.extend(items)
        self._create_menu()

    def update_menu_items(self, items: List[Dict[str, Any]]) -> None:
        self.menu_items = items
        self._create_menu()

    def open_menu(self) -> None:
        if self.is_open:
            self.close_menu()
        if self.menu and not self.menu.parent:
            self.menu.open()
            self.is_open = True

    def close_menu(self) -> None:
        if self.is_open and self.menu:
            self.menu.dismiss()
        self.is_open = False

    def menu_callback(self, text_item: str) -> None:
        self.ids.txt_field.text = text_item
        self.close_menu()

        if text_item in self._external_callbacks:
            for callback in self._external_callbacks[text_item]:
                if callable(callback):
                    callback(text_item)

    def on_release_items(self, text: str, callback: Callable, *args, **kwargs) -> None:
        if text not in self._external_callbacks:
            self._external_callbacks[text] = []

        if args or kwargs:
            wrapped_callback = lambda x: callback(x, *args, **kwargs)
        else:
            wrapped_callback = callback

        self._external_callbacks[text].append(wrapped_callback)
        self._create_menu()
    
    def on_release_all_items(self, callback: Callable, *args, **kwargs) -> None:
        for item in self.all_menu_items:
            self.on_release_items(item['text'], callback, *args, **kwargs)
    
    def remove_on_release_items(self, text: str, callback: Optional[Callable]=None) -> None:
        if text in self._external_callbacks:
            if callback is None:
                del self._external_callbacks[text]
            else:
                self._external_callbacks[text] = [
                    cb for cb in self._external_callbacks[text] 
                    if cb != callback
                ]
                if not self._external_callbacks[text]:
                    del self._external_callbacks[text]
        self._create_menu()
    
    def on_text(self, instance, text) -> None:
        self.on_validators(instance, text)

    def on_validators(self, instance, text) -> None:
        for validator in self.validators:
            check = validator(text)
            if not check.status:
                self.error = True
                self.helper_text = check.text
                self.helper_text_mode = 'on_error'
                break
        else:
            self.error = False
            self.helper_text = ''
            self.helper_text_mode = 'on_focus'
    
    def get_value(self) -> str:
        return self.ids.txt_field.text


class ChoiceSelectField(_BaseChoiceField):
    pass


class ChoiceFilterSelectField(_BaseChoiceField):
    def add_menu_items(self, items: List[Dict[str, Any]]) -> None:
        self.all_menu_items.extend(items)
        self.filter_items(refresh_only=True)

    def filter_items(self, refresh_only: bool = False) -> None:
        self.close_menu()

        if not refresh_only:
            value = self.ids.txt_field.text.lower()
            filtered_items = [
                item for item in self.all_menu_items 
                if value in item['text'].lower()
            ]
        else:
            filtered_items = self.all_menu_items.copy()

        self.menu_items = filtered_items
        if self.menu:
            try:
                if self.menu.parent:
                    self.menu.parent.remove_widget(self.menu)
                self.menu = None
            except:
                pass

        self._create_menu()
        if not refresh_only and self.ids.txt_field.focus:
            self.open_menu()
