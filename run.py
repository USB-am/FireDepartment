# -*- coding: utf-8 -*-

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')


import json

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from data_base import db, Tag, Rank, Position, Human, Emergency, \
	Worktype, ColorTheme
from data_base.base_records import write_records
from custom_screen import CustomScreen
from uix.screens.main_page import MainPage
from uix.screens.current_calls import CurrentCalls
from uix.screens.options import Options
from uix.screens.create_entry import CreateEntryTag, CreateEntryRank, \
	CreateEntryPosition, CreateEntryHuman, CreateEntryEmergency, \
	CreateEntryWorktype
from uix.screens.edit_entry_list import EditEntryList
from uix.screens.edit_entry import EditEntryTag, EditEntryRank, \
	EditEntryPosition, EditEntryHuman, EditEntryEmergency, EditEntryWorktype
from uix.screens.edit_color_theme import EditColorTheme
from uix.screens.global_options import GlobalOptions
from uix.screens.calls_list import CallsList


db.create_all()

write_records()


class PathManager:
	''' Менеджер путей перехода '''

	def __init__(self, screen_manager: ScreenManager):
		self.__screen_manager = screen_manager

		self.path = ['main_page', ]

	def forward(self, screen_name: str) -> Screen:
		print(f'{self.path[-1]} -> ', end='')
		self.__screen_manager.current = screen_name
		self.path.append(screen_name)
		print(screen_name)

		return self.__screen_manager.current_screen

	def back(self) -> Screen:
		if len(self.path) > 1:
			self.path.pop(-1)

		self.__screen_manager.current = self.path[-1]

		return self.__screen_manager.current_screen


class Application(MDApp):
	''' Главный класс приложения '''

	def __init__(self):
		super().__init__()

		self.screen_manager = ScreenManager()
		self.path_manager = PathManager(self.screen_manager)

		self.set_theme()
		self.setup()

	def setup(self) -> None:
		self.main_page = MainPage(self.path_manager)
		self.screen_manager.add_widget(self.main_page)
		self.screen_manager.current = 'main_page'

		self.current_calls = CurrentCalls(self.path_manager)
		self.screen_manager.add_widget(self.current_calls)

		self.options = Options(self.path_manager)
		self.screen_manager.add_widget(self.options)

		self.global_options = GlobalOptions(self.path_manager)
		self.screen_manager.add_widget(self.global_options)

		# Create screens
		for screen in (CreateEntryTag, CreateEntryRank, \
		               CreateEntryPosition, CreateEntryHuman, \
		               CreateEntryEmergency, CreateEntryWorktype
			):
			self.screen_manager.add_widget(screen(self.path_manager))

		# Edit screens_list
		for table in (Tag, Rank, Position, Human, Emergency, Worktype):
			self.screen_manager.add_widget(EditEntryList(
				self.path_manager, table
			))

		# Edit screens
		for screen in (EditEntryTag, EditEntryRank, EditEntryPosition, \
		               EditEntryHuman, EditEntryEmergency, EditEntryWorktype):
			self.screen_manager.add_widget(screen(self.path_manager))
		self.screen_manager.add_widget(EditColorTheme(
			self.path_manager, self.theme_cls
		))

		# Calls list
		self.screen_manager.add_widget(CallsList(self.path_manager))

	def set_theme(self) -> None:
		theme = ColorTheme.query.first()

		self.theme_cls.primary_palette = theme.primary_palette
		self.theme_cls.accent_palette = theme.accent_palette
		self.theme_cls.primary_hue = theme.primary_hue
		self.theme_cls.theme_style = theme.theme_style

		CustomScreen.color = json.loads(theme.background_color)
		CustomScreen.bg_image = theme.background_image

	def build(self) -> ScreenManager:
		return self.screen_manager


def main():
	app = Application()
	app.run()


if __name__ == '__main__':
	main()