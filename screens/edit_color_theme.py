from . import BaseScrolledScreen
from app.path_manager import PathManager
from data_base import ColorTheme


class EditColorTheme(BaseScrolledScreen):
	''' Экран кастомизации '''

	name = 'color_theme_edit'
	table = ColorTheme

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager
		self.__fill_toolbar()
		self.__fill_content()

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda e: self.path_manager.back()
		)

	def __fill_content(self) -> None:
		pass