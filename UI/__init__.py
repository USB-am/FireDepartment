# -*- coding: utf-8 -*-

# Temp import
import os
#os.environ['KIVY_NO_CONSOLELOG'] = '1'
from kivy.config import Config
Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from settings import settings as Settings
from .main_page import MainPage
from .options import Options
from .update_db_table.create_page import CreateTag, CreateRank, \
	CreatePosition, CreatePerson, CreatePost, CreateColorTheme


class Manager(ScreenManager):
	def __init__(self):
		super().__init__()

		# Main page
		self.add_widget(MainPage())

		# Options
		self.add_widget(Options())

		# Create pages
		self.add_widget(CreateTag())
		self.add_widget(CreateRank())
		self.add_widget(CreatePosition())
		self.add_widget(CreatePerson())
		self.add_widget(CreatePost())
		self.add_widget(CreateColorTheme())

		self.current = 'create_person'

	def move_to_back(self, x) -> None:
		to_page = Settings.PATH_MANAGER.back()
		self.current = to_page


class FireDepartment(MDApp):
	def build(self):
		return Manager()