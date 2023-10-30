from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from .path_manager import PathManager
from data_base import Emergency
from ui.screens import MainScreen, OptionsScreen, CallsScreen, \
	EmergencyList, \
	EmergencyEdit


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

		self.emergency_edit = EmergencyEdit(self.path_manager)
		self.screen_manager.add_widget(self.emergency_edit)
		self.emergencies_list = EmergencyList(self.path_manager)
		self.screen_manager.add_widget(self.emergencies_list)


		self.screen_manager.current = 'emergency_list'

	def build(self) -> ScreenManager:
		return self.screen_manager