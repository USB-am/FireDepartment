from . import SelectedScrollScreen
from app.path_manager import PathManager

import data_base
from ui.frames.list_items import FDEditModelListItem
from ui.fields.search import FDSearch


class _BaseEditModelListScreen(SelectedScrollScreen):
	''' Базовый класс списка редактируемых элементов '''

	_search_status = False

	def __init__(self, path_manager: PathManager):
		self.path_manager = path_manager
		self.search = FDSearch()

		super().__init__(self.search)

		self.__fill_toolbar()

		self.bind(on_pre_enter=lambda *e: self.__fill_content())
		self.search.bind_on_enter(self.search_entries)

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda e: self.path_manager.back()
		)

	def __fill_content(self) -> None:
		self.clear()

		self.add_widgets(*[FDEditModelListItem(entry) \
			for entry in self.table.query.all()])

	def search_entries(self) -> None:
		text = self.search.text
		self._search_status = bool(text)

		search_text = f'%{text}%'
		entries = self.table.query.filter(
			self.table.title.like(search_text)
		).all()
		
		self.clear()

		self.add_widgets(*[FDEditModelListItem(entry) \
			for entry in entries])

		self.update_back_button_callback()

	def update_back_button_callback(self) -> None:
		left_action_item = self.toolbar.left_action_items[0]
		if self._search_status:
			self.toolbar.remove_left_button()
			self.toolbar.add_left_button(
				icon='bus',
				callback=lambda e: self.reset_search()
			)
		else:
			self.toolbar.remove_left_button()
			self.toolbar.add_left_button(
				icon='arrow-left',
				callback=lambda e: self.path_manager.back()
			)

		self._search_status = not self._search_status

	def reset_search(self) -> None:
		self.search.text = ''
		self.search_entries()


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