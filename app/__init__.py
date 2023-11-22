from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout

from config import APP_SCREEN
from ui.screens.main import MainScreen
from ui.screens.options import OptionsScreen


Builder.load_file(APP_SCREEN)


class FDUIManager(MDNavigationLayout):
	''' Графический интерфейс приложения. '''

	@property
	def screen_manager(self) -> ScreenManager:
		return self.ids.screen_manager


class Application(MDApp):
	'''
	Базовый класс приложения. Инициализирует интерфейс и добавляет страницы.
	'''

	color = [1, 1, 1, 1]
	bg_image = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.ui = FDUIManager()
		self.ui.screen_manager.add_widget(MainScreen())
		self.ui.screen_manager.add_widget(OptionsScreen())

	def build(self):
		return self.ui