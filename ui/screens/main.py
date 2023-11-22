from . import BaseScreen, BaseScrollScreen
from kivymd.uix.label import MDLabel
from kivy.metrics import dp


class MainScreen(BaseScrollScreen):
	''' Стартовая страница '''

	name = 'main'
	toolbar_title = 'Главная'

	def __init__(self, **options):
		super().__init__()

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)
		for i in range(20):
			self.add_content(MDLabel(
				text=f'Row #{i+1}',
				size_hint=(1, None),
				height=dp(50)
			))
