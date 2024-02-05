from typing import Optional

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import NOTEBOOK_WIDGET
from data_base import Emergency
from .manager import NotebookManager, NotebookTab


Builder.load_file(NOTEBOOK_WIDGET)


class FDNotebook(MDBoxLayout):
	''' Виджет с табами '''

	def __init__(self, **options):
		super().__init__(**options)

		self._manager = NotebookManager(
			tab_panel=self.ids.tab_panel,
			phone_content=self.ids.phone_content,
			info_content=self.ids.info_content
		)

	def add_tab(self, emergency: Emergency) -> None:
		new_tab = self._manager.add_tab(emergency)

		self.ids.tab_panel.add_widget(new_tab.top_panel)

		self._manager.show_tab(new_tab)

	def get_current_tab(self) -> Optional[NotebookTab]:
		''' Возвращает текущую вкладку. '''

		if len(self._manager.tabs):
			return None

		for tab in self._manager.tabs:
			if tab.state:
				return tab
