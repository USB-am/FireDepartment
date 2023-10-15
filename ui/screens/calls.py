from kivy.lang.builder import Builder

from app.path_manager import PathManager
from data_base import Emergency
from ui.screens.base_screen import BaseScreen
from config.paths import __SCREEN_OPTIONS

Builder.load_file(__SCREEN_OPTIONS)


class CallsScreen(BaseScreen):
	''' Страница вызова на пожар '''

	name = 'calls'
	toolbar_title = 'Вызов'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(icon='arrow-left', callback=lambda e: path_manager.back())

	def display(self) -> None:
		print('All good!')
