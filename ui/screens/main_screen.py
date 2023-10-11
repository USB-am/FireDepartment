from app.path_manager import PathManager
from ui.screens.base_screen import BaseScreen
from ui.widgets.list_element import MainScreenElement
from data_base import Emergency


class MainScreen(BaseScreen):
	""" Главная страница """

	name = 'main'
	toolbar_title = 'Главная'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(icon='menu', callback=self.open_menu)

	def display(self) -> None:
		for i in range(10):
			e = Emergency(title=f'Emergency #{i+1}', description=f'Description Emergency #{i+1}', urgent=bool(i%2))
			w = MainScreenElement(emergency=e)
			self.add_content(w)