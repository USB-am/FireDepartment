from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from .path_manager import PathManager
from screens.main import MainScreen


class Application(MDApp):
	'''
	Главный класс приложения
	'''

	def __init__(self):
		super().__init__()
		self.screen_manager = ScreenManager()
		self.path_manager = PathManager(self.screen_manager)

		self.__add_screens()

	def __add_screens(self) -> None:
		self.main_screen = MainScreen(self.path_manager)
		self.screen_manager.add_widget(self.main_screen)
		self.screen_manager.current = 'main'

	def build(self) -> ScreenManager:
		return self.screen_manager