from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from .path_manager import PathManager
from ui.screens import MainScreen, OptionsScreen, CallsScreen


class Application(MDApp):
	''' Главный класс приложения '''

	def __init__(self):
		super().__init__()
		self.screen_manager = ScreenManager()
		self.path_manager = PathManager(self.screen_manager)

		self.__add_screens()

	def __add_screens(self) -> None:
		self.main_screen = MainScreen(self.path_manager)
		self.screen_manager.add_widget(self.main_screen)

		self.options_screen = OptionsScreen(self.path_manager)
		self.screen_manager.add_widget(self.options_screen)

		self.calls_screen = CallsScreen(self.path_manager)
		self.screen_manager.add_widget(self.calls_screen)

		self.screen_manager.current = 'main'

	def build(self) -> ScreenManager:
		return self.screen_manager