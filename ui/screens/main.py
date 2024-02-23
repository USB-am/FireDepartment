from . import BaseScrollScreen

from app.path_manager import PathManager
from data_base import Emergency
from ui.layout.main_screen import MainScreenListElement


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

		self.bind(on_pre_enter=lambda *_: self.fill_elements())

	def fill_elements(self) -> None:
		''' Заполнить контент Вызовами '''

		for emergency in Emergency.query.all():
			list_elem = MainScreenListElement(emergency)
			list_elem.bind_open_button(lambda e=emergency: self.open_call(e))
			self.add_content(list_elem)
		# self.ids.content.children = self.ids.content.children[::-1]

	def open_call(self, emergency: Emergency) -> None:
		'''
		Переходит на CallsScreen и добавляет вкладку на основании emergency.

		~params:
		emergency: Emergency - запись из БД о выезде.
		'''

		calls_screen = self._path_manager.forward('calls')
		calls_screen.notebook.add_tab(emergency)
