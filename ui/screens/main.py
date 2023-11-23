from . import BaseScreen, BaseScrollScreen
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from app.path_manager import PathManager


class MainScreen(BaseScrollScreen):
	''' Стартовая страница '''

	name = 'main'
	toolbar_title = 'Главная'

	def __init__(self, path_manager: PathManager, **options):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)
		self.ids.toolbar.add_right_button(
			icon='fire-truck',
			callback=lambda *_: self._path_manager.forward('calls')
		)

		for i in range(20):
			self.add_content(MDLabel(
				text=f'Row #{i+1}',
				size_hint=(1, None),
				height=dp(50)
			))