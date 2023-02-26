from kivy.lang.builder import Builder

from . import BaseScrolledScreen
from app.path_manager import PathManager


from . import SelectedScrollScreen
from ui.widgets import selection_elements


class MainScreen(SelectedScrollScreen):
	''' Главная страница '''

	name = 'main'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager
		self.__fill_toolbar()
		self.__fill_content()

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='fire-truck',
			callback=lambda event: print('fire-truck')
		)
		self.toolbar.add_right_button(
			icon='face-agent',
			callback=lambda event: self.path_manager.forward('options')
		)

	def __fill_content(self) -> None:
		elems = []
		for i in range(5):
			elems.append(selection_elements.FDOneLineElement(text=f'Element #{i+1}'))

		self.add_widgets(*elems)