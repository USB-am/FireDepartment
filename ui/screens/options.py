from . import BaseScreen


class OptionsScreen(BaseScreen):
	''' Страница с настройками '''

	name = 'options'
	toolbar_title = 'Настройки'

	def __init__(self, **options):
		super().__init__()

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)