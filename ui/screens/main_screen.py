from app.path_manager import PathManager
from ui.screens.base_screen import BaseScreen


class MainScreen(BaseScreen):
	""" Главная страница """

	name = 'main'
	toolbar_title = 'Главная'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(icon='menu', callback=self.open_menu)

	def display(self) -> None:
		pass