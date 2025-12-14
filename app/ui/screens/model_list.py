from typing import Any, Generator, List, Tuple
import time

from kivy.uix.widget import WidgetException
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base.model import db, Tag, Rank, Position, Human, Emergency, Worktype, Short
from ui.widgets.search import FDSearch
from ui.layout.model_list_element import ModelListElement
from ui.layout.dialogs import TagDialogContent, RankDialogContent, \
	PositionDialogContent, HumanDialogContent, EmergencyDialogContent,\
	WorktypeDialogContent, ShortDialogContent
from config import ITERABLE_COUNT


class Paginator:
	''' Пагинатор записей БД '''

	def __init__(self, *elements: Any):
		self.__all_elements = sorted(elements, key=lambda e: e.title)
		self.__current_elements = self.__all_elements.copy()

	def __str__(self):
		return self.__current_elements

	@property
	def all_elements(self) -> List[Any]:
		return self.__all_elements

	def paginate_by(self, count: int=10) -> Generator:
		'''
		Генератор элементов.

		~params:
		count: int=10 - количество элементов за одну итерацию.
		'''

		elements = self.__current_elements.copy()
		while elements:
			yield elements[:count]
			elements = elements[count:]

	def paginate_by_filter(self, elements: List[Any], count: int=10) -> Generator:
		'''
		Генератор отфильтрованных элементов.

		~params:
		elements: List[Any] - элементы для вывода пагинатора;
		count: int=10 - количество элементов на одну итерацию.
		'''

		self.__current_elements = elements
		return self.paginate_by(count)

	def append(self, element: Any) -> None:
		''' Добавить элемент в конец списка '''

		self.__all_elements = sorted(
			self.__all_elements + [element,],
			key=lambda e: e.entry.title
		)
		self.__current_elements = sorted(
			self.__current_elements + [element,],
			key=lambda e: e.entry.title
		)

	def reset_elements(self) -> None:
		self.__current_elements = self.__all_elements.copy()


class _ModelList(BaseScrollScreen):
	''' Базовый класс с элементами из базы данных '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		self.dialog = None
		self.paginator = Paginator()
		self.current_paginate = self.paginator.paginate_by(ITERABLE_COUNT)
		self.last_paginate_update = 0

		search = FDSearch(hint_text='Поиск...')
		search.on_press_enter(
			callback=lambda text: self.filter_by(text)
		)
		self.ids.content_container.add_widget(search)
		self.ids.content_container.children = self.ids.content_container.children[::-1]

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)
		self.ids.toolbar.add_right_button(
			icon='file-plus',
			callback=lambda *_: self._path_manager.forward(
				f'create_{self.model.__tablename__.lower()}'
		))

		self.bind(on_pre_enter=lambda *_: self.update_elements())

	def update_elements(self) -> None:
		''' Обновить элементы списка '''

		ids_for_delete, ids_for_insert = self.__check_new_elements()
		self.__delete_elements(ids_for_delete)
		self.__insert_elements(ids_for_insert)
		self.__show_elements()

	def end_list_event(self) -> None:
		''' Подгрузка элементов при прокрутке в конец страницы '''

		cur_time = time.time()
		if self.last_paginate_update <= cur_time - 1:
			self.last_paginate_update = cur_time
			self.__show_elements()

	def __check_new_elements(self) -> Tuple[set, set]:
		'''
		Проверка на новые элементы. Возвращает кортеж, где:
		Tuple[0] - список id записей для удаления;
		Tuple[1] - список id записей для добавления.
		'''

		all_ids = set(entry[0] for entry in \
			self.model.query.with_entities(self.model.id).all())
		old_ids = set(e.entry.id for e in self.ids.content.children)

		entries_for_insert = all_ids - old_ids
		entries_for_delete = old_ids - all_ids

		return entries_for_delete, entries_for_insert

	def __delete_elements(self, entries_for_delete: set) -> None:
		'''
		Удалить элементы списка.

		~params:
		entries_for_delete: set - множество элементов для удаления.
		'''

		layout = self.ids.content
		layout.clear_widgets()

		for element in self.paginator.all_elements:
			if element.entry.id not in entries_for_delete:
				layout.add_widget(element)

	def __insert_elements(self, entries_id_for_insert: set) -> None:
		'''
		Добавляет элементы в Paginator.

		~params:
		entries_id_for_insert: set - множество id записей для вставки.
		'''

		entries_for_insert = self.model.query.filter(self.model.id.in_(entries_id_for_insert))

		for entry_id in entries_id_for_insert:
			entry = self.model.query.get(entry_id)

			list_elem = ModelListElement(entry=entry, icon=self.model.icon)
			list_elem.bind_edit_btn(
				lambda e=entry: self.move_to_edit_and_fill_fields(e))
			list_elem.bind_info_btn(
				lambda e=entry: self.open_info_dialog(self.info_dialog_content(e))
			)

			self.paginator.append(list_elem)

	def __show_elements(self) -> None:
		''' Отобразить элементы '''

		try:
			for elem in next(self.current_paginate):
				try:
					self.ids.content.add_widget(elem)
				except AttributeError:
					pass
		except (StopIteration, WidgetException):
			pass

	def filter_by(self, title: str) -> None:
		'''
		Отфильтровать элементы по полю title.

		~params:
		title: str - часть текста поля title для поиска.
		'''

		all_ids = set(entry[0] for entry in \
			self.model.query.with_entities(self.model.id).all())

		elements = self.model.query\
			.filter(self.model.title.like(f'%{title}%'))\
			.order_by(self.model.title)
		new_ids = set(entry[0] for entry in \
			elements.with_entities(self.model.id).all())

		self.__delete_elements(all_ids - new_ids)

		all_elements = elements.all()
		filtered_elements = list(filter(
			lambda el: el.entry in all_elements,
			self.paginator.all_elements
		))
		self.current_paginate = self.paginator.paginate_by_filter(
			filtered_elements,
			count=ITERABLE_COUNT
		)
		self.__show_elements()

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
