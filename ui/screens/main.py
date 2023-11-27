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

		for emergency in Emergency.query.all():
			self.add_content(MainScreenListElement(emergency))
