from kivy.lang.builder import Builder

from . import BaseScrolledScreen, BaseBottomNavigationScreen
from app.path_manager import PathManager


class MainScreen(BaseBottomNavigationScreen):
	''' Главная страница '''

	name = 'main'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager
		self.bind(on_pre_enter=lambda e: self.__fill())

	def __fill(self) -> None:
		self.__fill_toolbar()
		self.__fill_content()

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='fire-truck',
			callback=lambda event: print('fire-truck')
		)
		self.toolbar.add_right_button(
			icon='face-agent',
			callback=lambda event: self.path_manager.forward('options')
		)

	def __fill_content(self) -> None:
		pass