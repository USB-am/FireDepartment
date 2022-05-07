# -*- coding: utf-8 -*-

# Temp import
from kivy.config import Config
Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from .screens import MainPage


class PathManager:
	PATH = ['main_page']

	def forward(self, page_name: str) -> None:
		self.PATH.append(page_name)

	def back(self) -> str:
		if len(self.PATH) > 1:
			self.PATH = self.PATH[:-1]

		return self.get_current_page_name

	def get_current_page_name(self) -> str:
		return self.PATH[-1]


class Manager(ScreenManager):
	def __init__(self):
		super().__init__()

		# Main page
		self.add_widget(MainPage())

		self.current = 'main_page'


class Application(MDApp):
	""" Running application """

	def __init__(self):
		super().__init__()

		self.path_manager = PathManager()
		self.screen_manager = Manager()

	def build(self) -> Manager:
		self.theme_cls.primary_palette = 'Indigo'#'Yellow'#
		self.theme_cls.accent_palette = 'Red'
		self.theme_cls.theme_style = 'Light'

		return self.screen_manager