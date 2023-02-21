from kivy.lang.builder import Builder
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

		self.entry = self._INPUT(**options)
		self.add_widget(self.entry)


class FDTextInput(BaseInput):
	''' Виджет ввода текста '''

	_INPUT = BaseTextInput


class FDNumInput(BaseInput):
	''' Виджет ввода цифр '''

	_INPUT = BaseNumInput