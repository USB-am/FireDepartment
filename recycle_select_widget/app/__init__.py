import os

from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationLayout

from .path_manager import PathManager
from screens.home import HomeScreen
from config import APP_KV


Builder.load_file(APP_KV)


class Interface(MDNavigationLayout):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.path_manager = PathManager(self.screen_manager)

	@property
	def screen_manager(self) -> ScreenManager:
		return self.ids.screen_manager


class Application(MDApp):
	title = 'Fire Department'

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.interface = Interface()

		self.interface.screen_manager.add_widget(HomeScreen())

	def build(self):
		return self.interface
