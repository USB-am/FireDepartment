# -*- coding: utf-8 -*-

from kivy.config import Config
Config.set('graphics', 'width', '350')


from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype
from data_base.base_records import write_records
from uix.screens.main_page import MainPage
from uix.screens.current_calls import CurrentCalls
from uix.screens.options import Options
from uix.screens.create_entry import CreateEntryTag, CreateEntryRank, CreateEntryPosition, \
	CreateEntryHuman, CreateEntryEmergency, CreateEntryWorktype
from uix.screens.edit_entry_list import EditEntryList
from uix.screens.edit_entry import EditEntryTag, EditEntryRank, EditEntryPosition, \
	EditEntryHuman, EditEntryEmergency, EditEntryWorktype, EditColorTheme


db.create_all()

write_records()


class PathManager:
	''' Менеджер путей перехода '''

	def __init__(self, screen_manager: ScreenManager):
		self.__screen_manager = screen_manager

		self.path = ['main_page', ]

	def forward(self, screen_name: str) -> Screen:
		self.__screen_manager.current = screen_name
		self.path.append(screen_name)

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

		self.setup()

		self.screen_manager.current = 'main_page'	# 'edit_colortheme'

	def setup(self) -> None:
		self.main_page = MainPage(self.path_manager)
		self.current_calls = CurrentCalls(self.path_manager)
		self.options = Options(self.path_manager)

		# Create screens
		for screen in (CreateEntryTag, CreateEntryRank, CreateEntryPosition, \
		               CreateEntryHuman, CreateEntryEmergency, CreateEntryWorktype):
			self.screen_manager.add_widget(screen(self.path_manager))

		# Edit screens_list
		for table in (Tag, Rank, Position, Human, Emergency, Worktype):
			self.screen_manager.add_widget(EditEntryList(self.path_manager, table))

		# Edit screens
		for screen in (EditEntryTag, EditEntryRank, EditEntryPosition, \
		               EditEntryHuman, EditEntryEmergency, EditEntryWorktype):
			self.screen_manager.add_widget(screen(self.path_manager))
		self.screen_manager.add_widget(EditColorTheme(self.path_manager, self.theme_cls))

		self.screen_manager.add_widget(self.main_page)
		self.screen_manager.add_widget(self.current_calls)
		self.screen_manager.add_widget(self.options)

	def build(self) -> ScreenManager:
		return self.screen_manager


def main():
	app = Application()
	app.run()


if __name__ == '__main__':
	main()