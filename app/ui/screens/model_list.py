from typing import Any, Generator, List, Tuple
import time

from kivy.uix.widget import WidgetException
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from .base import BaseScrollScreen
from ui.widgets.search import FDSearch
from ui.layout.model_list_element import ModelListElement
# from ui.layout.dialogs import TagDialogContent, RankDialogContent, \
# 	PositionDialogContent, HumanDialogContent, EmergencyDialogContent,\
# 	WorktypeDialogContent, ShortDialogContent
from service.server import send_get


class _ModelList(BaseScrollScreen):
	''' Базовый класс с элементами из базы данных '''

	def __init__(self, path_manager: 'PathManager'):
		super().__init__(path_manager)
		self.dialog = None

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
				f'create_{self.model.lower()}'
		))

		# self.update_elements()
		self.bind(on_pre_enter=lambda e: self.update_elements())

	def update_elements(self) -> None:
		''' Обновить элементы '''
		entries = send_get('model', params={
			'model': self.model
		}).json()

		for entry in entries:
			content = self.ids.content
			content.add_widget(ModelListElement(entry))

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

	def move_to_edit_and_fill_fields(self, entry: 'db.Model') -> None:
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
	model = 'Tag'
	toolbar_title = 'Теги'
	# info_dialog_content = TagDialogContent


class ShortsList(_ModelList):
	''' Класс с элементами из модели Short '''

	name = 'shorts_list'
	model = 'Short'
	toolbar_title = 'Сокращения'
	# info_dialog_content = ShortDialogContent


class RanksList(_ModelList):
	''' Класс с элементами из модели Rank '''

	name = 'ranks_list'
	model = 'Rank'
	toolbar_title = 'Звания'
	# info_dialog_content = RankDialogContent


class PositionsList(_ModelList):
	''' Класс с элементами из модели Position '''

	name = 'positions_list'
	model = 'Position'
	toolbar_title = 'Должности'
	# info_dialog_content = PositionDialogContent


class HumansList(_ModelList):
	''' Класс с элементами из модели Human '''

	name = 'humans_list'
	model = 'Human'
	toolbar_title = 'Сотрудники'
	# info_dialog_content = HumanDialogContent


class EmergenciesList(_ModelList):
	''' Класс с элементами из модели Emergency '''

	name = 'emergencies_list'
	model = 'Emergency'
	toolbar_title = 'Вызовы'
	# info_dialog_content = EmergencyDialogContent


class WorktypesList(_ModelList):
	''' Класс с элементами из модели Worktype '''

	name = 'worktypes_list'
	model = 'Worktype'
	toolbar_title = 'Графики работы'
	# info_dialog_content = WorktypeDialogContent
