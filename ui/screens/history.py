from . import BaseScrollScreen
from app.path_manager import PathManager


class History(BaseScrollScreen):
	''' Экран с историей завершенных вызовов '''

	name = 'history'
	toolbar_title = 'История Вызовов'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)
