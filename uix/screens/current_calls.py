from custom_screen import CustomScreen

from config import LOCALIZED
from uix import FDNoteBook, FDEmergencyTab, FDEmptyTab
from data_base import db


class CurrentCalls(CustomScreen):
	''' Экран текущих вызовов '''

	name = 'current_calls'

	def __init__(self, path_manager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Current calls')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())
		self.toolbar.add_right_button('check-outline', lambda e: self.close_tab())

		self.notebook = FDNoteBook()
		self.add_widgets(self.notebook)

	def add_tab(self, element: db.Model) -> None:
		self.notebook.add_tab(FDEmergencyTab(element))
		self.notebook.switch_to_last_tab()

	def close_tab(self) -> None:
		current_tab = self.notebook.current_tab
		self.notebook.close_tab(current_tab)