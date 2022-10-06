from custom_screen import CustomScreen

from config import LOCALIZED
from uix import FDNoteBook, FDEmergencyTab
from data_base import db


class CurrentCalls(CustomScreen):
	''' Экран текущих вызовов '''

	name = 'current_calls'

	def __init__(self, path_manager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Current calls')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())
		self.toolbar.add_right_button('check-outline', lambda e: self.close_tab())

	def fill_content(self) -> None:
		self.notebook = FDNoteBook()
		self.add_widgets(self.notebook)

	def add_tab(self, element: db.Model) -> None:
		self.notebook.add_widget(FDEmergencyTab(element))
		self.notebook.switch_tab(self.notebook.get_tab_list()[-1])

	def close_tab(self) -> None:
		if len(self.notebook.get_tab_list()) > 1:
			current_tab = self.notebook.current_tab
			self.notebook.remove_widget(current_tab)

		else:
			print(':c')