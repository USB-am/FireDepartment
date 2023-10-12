from app.path_manager import PathManager
from data_base import Emergency
from ui.screens.base_screen import BaseScreen
from ui.widgets.list_element import MainScreenElement


class MainScreen(BaseScreen):
	""" Главная страница """

	name = 'main'
	toolbar_title = 'Главная'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(icon='menu', callback=self.open_menu)
		self.ids.toolbar.add_right_button(icon='fire-truck', callback=lambda e: path_manager.forward('calls'))

	def display(self) -> None:
		for emergency in Emergency.query.all():
			self.add_content(MainScreenElement(emergency))