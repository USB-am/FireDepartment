from typing import List, Callable

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from config import SEARCH_WIDGET


Builder.load_file(SEARCH_WIDGET)


class _SearchTextFeild(MDTextField):
	''' Текстовое поле поиска '''

	def __init__(self, **options):
		super().__init__(**options)

		self.callbacks: List[Callable] = []

	def on_text_validate(self) -> None:
		''' Событие нажатия Enter '''

		output = super().on_text_validate()

		# Вызов событий
		for callback in self.callbacks:
			callback(self.text)

		return output


class FDSearch(MDBoxLayout):
	''' Поле поискового ввода '''

	def __init__(self, **options):
		super().__init__()

		self.field = _SearchTextFeild(**options)
		self.add_widget(self.field)

	def on_press_enter(self, callback: Callable) -> None:
		''' Добавить событие при нажатии Enter '''

		self.field.callbacks.append(callback)
