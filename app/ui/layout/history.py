from typing import Callable

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import HISTORY_LAYOUT


Builder.load_file(HISTORY_LAYOUT)


class FDHistoryElement(MDBoxLayout):
	''' Элемент на экране history '''

	title = StringProperty()

	def bind_btn(self, callback: Callable) -> None:
		''' Привязать событие к нажатию кнопки '''

		self.ids.btn.bind(on_release=lambda *_: callback())
