from . import SelectedScrollScreen
from app.path_manager import PathManager

import data_base
from ui.frames.list_items import FDEditModelListItem
from ui.fields.search import FDSearch


class _BaseEditModelListScreen(SelectedScrollScreen):
	''' Базовый класс списка редактируемых элементов '''

	def __init__(self, path_manager: PathManager):
		self.path_manager = path_manager
		self.search = FDSearch()

		super().__init__(self.search)

		self.__fill_toolbar()

		self.bind(on_pre_enter=lambda *e: self.__fill_content())

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda e: self.path_manager.back()
		)

	def __fill_content(self) -> None:
		self.clear()

		self.add_widgets(*[FDEditModelListItem(entry) \
			for entry in self.table.query.all()])


class EditTagListScreen(_BaseEditModelListScreen):
	''' Список редактируемых Тегов '''

	name = 'edit_tag_list'
	table = data_base.Tag


class EditRankListScreen(_BaseEditModelListScreen):
	''' Список редактируемых Званий '''

	name = 'edit_rank_list'
	table = data_base.Rank


class EditPositionListScreen(_BaseEditModelListScreen):
	''' Список редактируемых Должностей '''

	name = 'edit_position_list'
	table = data_base.Position


class EditHumanListScreen(_BaseEditModelListScreen):
	''' Список редактируемых Людей '''

	name = 'edit_human_list'
	table = data_base.Human


class EditEmergencyListScreen(_BaseEditModelListScreen):
	''' Список редактируемых Вызовов '''

	name = 'edit_emergency_list'
	table = data_base.Emergency


class EditWorktypeListScreen(_BaseEditModelListScreen):
	''' Список редактируемых Графиков работ '''

	name = 'edit_worktype_list'
	table = data_base.Worktype