from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel

from . import BaseScrolledScreen
from app.path_manager import PathManager


class OptionsScreen(BaseScrolledScreen):
	''' Главная страница '''

	name = 'options'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager
		self.__fill_toolbar()

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda event: self.path_manager.back()
		)