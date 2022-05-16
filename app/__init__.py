# -*- coding: utf-8 -*-

# Temp import
from kivy.config import Config
Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from .screens import MainPage, Settings, CreateTag, CreateRank,\
	CreatePosition, CreateHuman, CreateEmergency, CreateColorTheme,\
	CreateWorkType


class PathManager:
	PATH = ['main_page']

	def forward(self, page_name: str) -> None:
		self.PATH.append(page_name)

	def back(self) -> str:
		if len(self.PATH) > 1:
			self.PATH = self.PATH[:-1]

		return self.get_current_page_name

	@property
	def get_current_page_name(self) -> str:
		return self.PATH[-1]


class Manager(ScreenManager):
	def __init__(self):
		super().__init__()

		# Main page
		self.add_widget(MainPage())

		# Settings
		self.add_widget(Settings())

		# Create screens
		self.add_widget(CreateTag())
		self.add_widget(CreateRank())
		self.add_widget(CreatePosition())
		self.add_widget(CreateHuman())
		self.add_widget(CreateEmergency())
		self.add_widget(CreateColorTheme())
		self.add_widget(CreateWorkType())

		self.current = 'create_emergency'


class Application(MDApp):
	""" Running application """

	def __init__(self):
		super().__init__()

		self.screen_manager = Manager()
		self.path_manager = PathManager()

	def forward(self, page_name: str) -> None:
		self.path_manager.forward(page_name)
		self.screen_manager.current = page_name

	def back(self) -> str:
		current_page_name = self.path_manager.back()
		self.screen_manager.current = current_page_name

		return current_page_name

	def build(self) -> Manager:
		self.theme_cls.primary_palette = 'BlueGray'#'Indigo'#
		self.theme_cls.accent_palette = 'Teal'
		self.theme_cls.theme_style = 'Light'

		return self.screen_manager