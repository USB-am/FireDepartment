from typing import Callable

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import NOTEBOOK_WIDGET


Builder.load_file(NOTEBOOK_WIDGET)


class _NotebookManager:
	''' Менеджер табов и контента FDNotebook '''

	def __init__(self):
		self.tags = []
		self.content = []


class NotebookTab(MDBoxLayout):
	''' Таб верхней панели FDNotebook'а '''

	title = StringProperty()


class FDNotebook(MDBoxLayout):
	''' Виджет с табами '''

	def __init__(self, **options):
		super().__init__(**options)

		self.__manager = _NotebookManager()

	def add_tab(self, title: str, callback: Callable) -> None:
		new_tab = NotebookTab(title=title)
		self.ids.tab_panel.add_widget(new_tab)
