from . import BaseScreen


class MainScreen(BaseScreen):
	''' Стартовая страница '''

	name = 'main'
	toolbar_title = 'Главная'

	def __init__(self, **options):
		super().__init__()

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)