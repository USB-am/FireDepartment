from typing import Union

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout

from config import paths
from config.localizer import LOCALIZE


Builder.load_file(paths.TEXT_INPUT_FIELD)


class BaseTextInput(MDTextField):
	''' Базовое поле ввода текста '''


class BaseNumInput(MDTextField):
	''' Базовое поле ввода цифр '''

	def insert_text(self, substring: str, from_undo: bool=False) -> None:
		s = substring if substring.isdigit() else ''

		return super().insert_text(s, from_undo)


class BaseInput(MDBoxLayout):
	''' Базовая область отображения полей ввода '''

	_INPUT = BaseTextInput

	def __init__(self, **options):
		super().__init__()

		self.entry = self._INPUT(
			icon_right=self.right_icon,
			**options
		)
		self.add_widget(self.entry)

	def get_value(self) -> Union[str, None]:
		inner_text = self.entry.text

		return inner_text if inner_text else None

	def set_value(self, value: str) -> None:
		if value is None:
			value = ''

		self.entry.text = value


class FDTextInput(BaseInput):
	''' Виджет ввода текста '''

	_INPUT = BaseTextInput
	right_icon = StringProperty('format-text')


class FDNumInput(BaseInput):
	''' Виджет ввода цифр '''

	_INPUT = BaseNumInput
	right_icon = StringProperty('numeric')


class FDDescriptionInput(BaseInput):
	''' Виджет ввода многострочного текста '''

	_INPUT = BaseTextInput
	right_icon = StringProperty('text')