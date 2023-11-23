from . import BaseScreen
from app.path_manager import PathManager


class OptionsScreen(BaseScreen):
	''' Страница с настройками '''

	name = 'options'
	toolbar_title = 'Настройки'

	def __init__(self, path_manager: PathManager, **options):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)