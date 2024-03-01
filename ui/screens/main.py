from typing import List

from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base import Emergency
from ui.layout.main_screen import MainScreenListElement
from ui.widgets.search import FDSearch


def filter_list_elements(text: str) -> List[Emergency]:
	'''
	Отфильтровать элементы списка по названию из text.

	~params:
	text: str - текст поиска.
	'''

	filtered_emergencies = Emergency.query.filter(
		Emergency.title.like(f'%{text}%')
	).order_by(Emergency.title).all()

	return filtered_emergencies


class MainScreen(BaseScrollScreen):
	''' Стартовая страница '''

	name = 'main'
	toolbar_title = 'Главная'

	def __init__(self, path_manager: PathManager, **options):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)
		self.ids.toolbar.add_right_button(
			icon='fire-truck',
			callback=lambda *_: self._path_manager.forward('calls')
		)

		search = FDSearch(hint_text='Поиск...')
		search.on_press_enter(
			callback=lambda text: self.__hide_elements(
				filter_list_elements(text)
			)
		)
		self.ids.content_container.add_widget(search)
		self.ids.content_container.children = self.ids.content_container.children[::-1]

		self.elements: List[MainScreenListElement] = []
		self.bind(on_pre_enter=lambda *_: self.fill_elements())

	def fill_elements(self) -> None:
		''' Заполнить контент Вызовами '''

		for emergency in Emergency.query.order_by(Emergency.title).all():
			list_elem = MainScreenListElement(emergency)
			list_elem.bind_open_button(lambda e=emergency: self.open_call(e))
			self.elements.append(list_elem)
			self.add_content(list_elem)

	def __hide_elements(self, filtered_elements: List[Emergency]) -> None:
		'''
		Скрыть элементы списка.

		~params:
		elements: List[Emergency] - записи БД, элементы которых необходимо скрыть.
		'''

		layout: List[MainScreenListElement] = self.ids.content
		layout.clear_widgets()

		for element in self.elements:
			if element.emergency in filtered_elements:
				self.add_content(element)

	def open_call(self, emergency: Emergency) -> None:
		'''
		Переходит на CallsScreen и добавляет вкладку на основании emergency.

		~params:
		emergency: Emergency - запись из БД о выезде.
		'''

		calls_screen = self._path_manager.forward('calls')
		calls_screen.notebook.add_tab(emergency)
