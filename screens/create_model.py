from app.path_manager import PathManager
import data_base
from . import BaseScrolledScreen


class _BaseCreateModelScreen(BaseScrolledScreen):
	''' Базовое представление экрана создания '''

	def __init__(self, path_manager: PathManager):
		self.path_manager = path_manager

		super().__init__()

		self.__fill_toolbar()

		self.bind(on_pre_enter=lambda *e: self.__fill_content())

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda e: self.path_manager.back()
		)

	def __fill_content(self) -> None:
		pass


class CreateTagScreen(_BaseCreateModelScreen):
	''' Экран создания тега '''

	name = 'create_tag'
	table = data_base.Tag