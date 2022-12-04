from custom_screen import CustomScrolledScreen
from config import LOCALIZED
from uix import fields
# from data_base import Calls


class CallsList(CustomScrolledScreen):
	''' Страница со списком всех вызовов '''

	name = 'calls_list'

	def __init__(self, path_manager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Calls list')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())

	def fill_content(self) -> None:
		pass