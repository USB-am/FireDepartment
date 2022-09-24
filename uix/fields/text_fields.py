from typing import Union

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from config import LOCALIZED, HELP_MODE
from uix.help_button import HelpButton


class _BaseString(MDTextField):
	''' Текстовое поле '''

	def __init__(self, title: str, **options):
		self.title = title

		super().__init__(**options)

		self.icon_right = 'form-textbox'
		self.hint_text = LOCALIZED.translate(title)

	def add_right_icon(self, icon: str) -> None:
		self.icon_right = icon

	def set_value(self, value: str) -> None:
		self.ids.entry.text = '-' if value is None else value

	def get_value(self) -> str:
		value = self.ids.entry.text

		return None if value == '-' else value


class _OnlyIntegerString(_BaseString):
	''' Текстовое поле, содержащее ТОЛЬКО цифры '''

	def insert_text(self, substring: str, from_undo=False) -> None:
		if substring.isdigit():
			super().insert_text(substring, from_undo=from_undo)


class StringField(MDBoxLayout):
	''' Текстовое поле '''

	def __init__(self, title: str, help_text: str=None, 
		         string_obj: Union[_BaseString, _OnlyIntegerString]=_BaseString,
		         **options):

		self.title = title
		options.update({
			'icon_right': 'form-textbox',
			'hint_text': LOCALIZED.translate(title)
		})

		super().__init__(size_hint=(1, None),size=(self.width, 50))

		self.base_string = string_obj(title, **options)
		self.add_widget(self.base_string)

		if help_text is not None and HELP_MODE:
			self.add_widget(HelpButton(
				title=self.__class__.__name__,
				text=help_text))

	def add_right_icon(self, icon: str) -> None:
		self.base_string.icon_right = icon

	def set_value(self, value: str) -> None:
		self.base_string.text = '-' if value is None else value

	def get_value(self) -> str:
		value = self.base_string.text

		return None if value == '-' else value


class PhoneField(StringField):
	''' Текстовое поле ввода телефона '''

	def __init__(self, title: str, help_text: str=None):
		super().__init__(title, help_text)

		self.add_right_icon('phone')


class DescriptionField(StringField):
	''' Многострочное поле '''

	def __init__(self, title: str, help_text: str=None):
		super().__init__(title, help_text, multiline=True, max_height=100)

		self.add_right_icon('text-long')


class IntegerField(StringField):
	''' Поле ввода целых чисел '''

	def __init__(self, title: str, help_text: str=None):
		super().__init__(title, help_text, _OnlyIntegerString)

		self.add_right_icon('numeric')