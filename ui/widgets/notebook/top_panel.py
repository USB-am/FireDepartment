from typing import Callable

from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


class NotebookTopPanelElement(MDBoxLayout):
	''' Таб верхней панели FDNotebook'а '''

	title = StringProperty()

	def bind_open(self, callback: Callable) -> None:
		'''
		Привязывает событие к нажатию кнопки открытия.

		~params:
		callback: Callable - событие, которое будет вызываться при нажатии.
		'''

		self.ids.tab_title.bind(on_release=lambda *_: callback())

	def bind_close(self, callback: Callable) -> None:
		'''
		Привязывает событие к нажатию кнопки закрытия.

		~params:
		callback: Callable - событие, которое будет вызываться при нажатии.
		'''

		self.ids.close_btn.bind(on_release=lambda *_: callback())
