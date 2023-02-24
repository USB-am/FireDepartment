from kivy.lang.builder import Builder

from . import BaseScrolledScreen
from app.path_manager import PathManager
from ui.fields.entry import FDTextInput, FDNumInput
from ui.fields.select_list import FDSelectList

from data_base import db, Human
from kivymd.uix.button import MDFlatButton


class MainScreen(BaseScrolledScreen):
	''' Главная страница '''

	name = 'main'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager
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