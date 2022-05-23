# -*- coding: utf-8 -*-

# Temp import
from kivy.config import Config
Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from app.tools.path_manager import PathManager
from .screens import \
	MainPage,\
	Settings,\
	UpdateColorTheme,\
	CreateTag, CreateRank, CreatePosition, CreateHuman, CreateEmergency,\
	CreateWorkType,\
	UpdateListTag, UpdateListRank, UpdateListPosition,\
	UpdateListHuman, UpdateListEmergency, UpdateListWorkType,\
	EditTag, EditRank, EditPosition, EditHuman, EditEmergency, EditWorkType


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
		self.add_widget(CreateWorkType())

		# Update list screens
		self.add_widget(UpdateListTag())
		self.add_widget(UpdateListRank())
		self.add_widget(UpdateListPosition())
		self.add_widget(UpdateListHuman())
		self.add_widget(UpdateListEmergency())
		self.add_widget(UpdateListWorkType())

		# Edit screens
		self.add_widget(EditTag())
		self.add_widget(EditRank())
		self.add_widget(EditPosition())
		self.add_widget(EditHuman())
		self.add_widget(EditEmergency())
		self.add_widget(EditWorkType())

		# Update color theme
		self.add_widget(UpdateColorTheme())

		self.current = 'settings'


class Application(MDApp):
	""" Running application """

	def __init__(self):
		super().__init__()

		self.screen_manager = Manager()

	def forward(self, page_name: str) -> None:
		PathManager.forward(page_name)
		self.screen_manager.current = page_name

	def back(self) -> str:
		current_page_name = PathManager.back()
		self.screen_manager.current = current_page_name

		return current_page_name

	def build(self) -> Manager:
		self.theme_cls.primary_palette = 'BlueGray'
		self.theme_cls.accent_palette = 'Teal'
		self.theme_cls.theme_style = 'Light'

		return self.screen_manager

	def on_start(self):
		self.fps_monitor_start()