from . import SelectedScrollScreen
from app.path_manager import PathManager

import data_base
from ui.frames.list_items import FDEditModelListItem


class _BaseEditModelListScreen(SelectedScrollScreen):
	''' Базовый класс списка редактируемых элементов '''

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
		self.add_widgets(*[FDEditModelListItem(entry) \
			for entry in self.table.query.all()])


class EditTagListScreen(_BaseEditModelListScreen):
	''' Список редактируемых Тегов '''

	name = 'edit_tag_list'
	table = data_base.Tag


class EditHumanListScreen(_BaseEditModelListScreen):
	''' Список редактируемых Людей '''

	name = 'edit_human_list'
	table = data_base.Human