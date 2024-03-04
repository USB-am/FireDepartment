from typing import List

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype, Short
from ui.layout.model_list_element import ModelListElement
from ui.layout.dialogs import TagDialogContent, RankDialogContent, \
	PositionDialogContent, HumanDialogContent, EmergencyDialogContent,\
	WorktypeDialogContent, ShortDialogContent


class _ModelList(BaseScrollScreen):
	''' Базовый класс с элементами из базы данных '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		self.dialog = None

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)
		self.ids.toolbar.add_right_button(
			icon='file-plus',
			callback=lambda *_: self._path_manager.forward(
				f'create_{self.model.__tablename__.lower()}'
		))

		self.bind(on_pre_enter=lambda *_: self.__check_new_elements())

	def end_list_event(self) -> None:
		''' Подгрузка элементов при прокрутке в конец страницы '''

		print('_ModelList.end_list_event')

	def __check_new_elements(self) -> None:
		''' Проверка на новые элементы '''

		all_ids = set(entry[0] for entry in \
			self.model.query.with_entities(self.model.id).all())
		old_ids = set(e.entry.id for e in self.ids.content.children)

		entries_for_insert = all_ids - old_ids
		entries_for_delete = old_ids - all_ids
		self.__delete_elements(entries_for_delete)
		self.__insert_elements(entries_for_insert)

	def __delete_elements(self, entries_for_delete: set) -> None:
		'''
		Удалить элементы списка.

		~params:
		entries_for_delete: set - множество элементов для удаления.
		'''

		for element in self.ids.content.children:
			if element.entry.id in entries_for_delete:
				self.ids.content.remove_widget(element)
				del element

	def __insert_elements(self, entries_for_insert: set) -> None:
		'''
		Вставить элементы списка.

		~params:
		entries_for_insert: set - множество элементов для вставки.
		'''

		for entry_id in entries_for_insert:
			entry = self.model.query.get(entry_id)
			# list_elem = MainScreenListElement(entry)
			# list_elem.bind_open_button(lambda e=entry: self.open_call(e))
			list_elem = ModelListElement(entry=entry, icon=self.model.icon)
			list_elem.bind_edit_btn(
				lambda e=entry: self.move_to_edit_and_fill_fields(e))
			list_elem.bind_info_btn(
				lambda e=entry: self.open_info_dialog(self.info_dialog_content(e))
			)
			self.add_content(list_elem)

		childs = self.ids.content.children
		self.ids.content.children = sorted(
			self.ids.content.children,
			key=lambda child: child.entry.title,
			reverse=True
		)

	def open_info_dialog(self, content: MDBoxLayout) -> None:
		''' Открыть диалогов окно с информацией '''

		ok_btn = MDRaisedButton(text='Ок')
		dialog = MDDialog(
			title='Информация',
			type='custom',
			content_cls=content,
			buttons=[ok_btn]
		)
		ok_btn.bind(on_release=lambda *_: dialog.dismiss())

		dialog.open()

	def move_to_edit_and_fill_fields(self, entry: db.Model) -> None:
		'''
		Перейти на экран редактирования записи.

		~params:
		entry: db.Model - запись, которая будет редактироваться.
		'''

		next_screen = self._path_manager.forward(
			f'edit_{self.model.__tablename__.lower()}')
		next_screen.fill_fields(entry)


class TagsList(_ModelList):
	''' Класс с элементами из модели Tag '''

	name = 'tags_list'
	model = Tag
	toolbar_title = 'Теги'
	info_dialog_content = TagDialogContent


class ShortsList(_ModelList):
	''' Класс с элементами из модели Short '''

	name = 'shorts_list'
	model = Short
	toolbar_title = 'Сокращения'
	info_dialog_content = ShortDialogContent


class RanksList(_ModelList):
	''' Класс с элементами из модели Rank '''

	name = 'ranks_list'
	model = Rank
	toolbar_title = 'Звания'
	info_dialog_content = RankDialogContent


class PositionsList(_ModelList):
	''' Класс с элементами из модели Position '''

	name = 'positions_list'
	model = Position
	toolbar_title = 'Должности'
	info_dialog_content = PositionDialogContent


class HumansList(_ModelList):
	''' Класс с элементами из модели Human '''

	name = 'humans_list'
	model = Human
	toolbar_title = 'Сотрудники'
	info_dialog_content = HumanDialogContent


class EmergenciesList(_ModelList):
	''' Класс с элементами из модели Emergency '''

	name = 'emergencies_list'
	model = Emergency
	toolbar_title = 'Вызовы'
	info_dialog_content = EmergencyDialogContent


class WorktypesList(_ModelList):
	''' Класс с элементами из модели Worktype '''

	name = 'worktypes_list'
	model = Worktype
	toolbar_title = 'Графики работы'
	info_dialog_content = WorktypeDialogContent
