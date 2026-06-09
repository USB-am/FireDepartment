from typing import List

from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.relativelayout import MDRelativeLayout

from . import _BaseWidget
from validators.widgets import BaseValidator


Builder.load_string('''
<FDTextInput>:
    helper_text_mode: 'persistent'
    on_text: root.custom_validate(self, self.text)
    on_focus: root.custom_validate(self, self.text)


<FDPasswordInput>:
    size_hint: (1, None)
    height: text_field.height

    MDTextField:
        id: text_field
        hint_text: root.hint_text
        password: True
        on_text: root.custom_validate(self, self.text)
        on_focus: root.custom_validate(self, self.text)

    MDIconButton:
        icon: 'eye-off'
        pos_hint: {'center_y': .5}
        pos: (text_field.width - self.width + dp(8), 0)
        on_release:
            self.icon = 'eye' if self.icon == 'eye-off' else 'eye-off'
            text_field.password = not text_field.password
''')


def _validate(instance: MDTextField, value: str, validators: List[BaseValidator]) -> None:
    for validator in validators:
        result = validator(value)

        if not result.status:
            instance.error = True
            instance.helper_text = result.message
            return

    else:
        instance.error = False
        instance.helper_text = ''


class FDTextInput(MDTextField, _BaseWidget):
    ''' Текстовое поле '''
    hint_text = StringProperty()
    helper_text = StringProperty('')

    def get_value(self) -> str:
        return self.text

    def custom_validate(self, instance: MDTextField, value: str) -> None:
        return _validate(instance, value, self.validators)


class FDPasswordInput(MDRelativeLayout, _BaseWidget):
    ''' Текстовое поле ввода пароля '''
    hint_text = StringProperty()
    helper_text = StringProperty('')

    def get_value(self) -> str:
        return self.ids.text_field.text

    def custom_validate(self, instance: MDTextField, value: str) -> None:
        return _validate(instance, value, self.validators)
