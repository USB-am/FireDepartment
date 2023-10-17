from kivymd.uix.button import MDIconButton

from app.path_manager import PathManager
from ui.screens.base_screen import BaseScreen
from ui.widgets.notebook import FDNotebook


class CallsScreen(BaseScreen):
	''' Страница вызова на пожар '''

	name = 'calls'
	toolbar_title = 'Вызовы'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda e: path_manager.back()
		)

	def display(self) -> None:
		self.add_fixed_widget(MDIconButton(icon='phone'))
		self.add_content(FDNotebook())
