# -*- coding: utf-8 -*-

# Temp import
from kivy.config import Config
Config.set('graphics', 'width', '350')


from typing import Union

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from custom_screen import CustomScreen, CustomScrolledScreen
from config import LOCALIZED
from uix import FDSearchBlock, FDExpansionPanel, \
	ExpansionEmergencyElement, ExpansionOptionsElement, FDNoteBook, FDEmergencyTab
from data_base import db, Tag, Rank, Position, Human, Emergency


db.create_all()


class PathManager:
	''' Менеджер путей перехода '''

	def __init__(self, screen_manager: ScreenManager):
		self.__screen_manager = screen_manager

		self.path = ['main_page', ]

	def forward(self, screen_name: str) -> Union[CustomScreen, CustomScrolledScreen]:
		self.__screen_manager.current = screen_name
		self.path.append(screen_name)

		return self.__screen_manager.current_screen

	def back(self) -> Union[CustomScreen, CustomScrolledScreen]:
		if len(self.path) > 1:
			self.path.pop(-1)

		self.__screen_manager.current = self.path[-1]

		return self.__screen_manager.current_screen


class MainPage(CustomScrolledScreen):
	''' Главный экран '''

	name = 'main_page'

	def __init__(self, path_manager: PathManager):
		self.search_block = FDSearchBlock()

		super().__init__(self.search_block)

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Main')
		self.toolbar.add_left_button('fire-truck',
			lambda e: self.path_manager.forward('current_calls'))
		self.toolbar.add_right_button('cog',
			lambda e: self.path_manager.forward('options'))

	def fill_content(self) -> None:
		for emergency in Emergency.query.all():
			element = FDExpansionPanel(emergency, ExpansionEmergencyElement)
			self.add_widgets(element)


class CurrentCalls(CustomScreen):
	''' Экран текущих вызовов '''

	name = 'current_calls'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Current calls')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())
		self.toolbar.add_right_button('check-outline', lambda e: print('Done'))

	def fill_content(self) -> None:
		self.notebook = FDNoteBook()
		self.add_widgets(self.notebook)

	def add_tab(self, element: db.Model) -> None:
		self.notebook.add_widget(FDEmergencyTab(element))


class Options(CustomScrolledScreen):
	''' Экран настроек '''

	name = 'options'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Options')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())

	def fill_content(self) -> None:
		for data_base_table in (Tag, Rank, Position, Human, Emergency):
			element = FDExpansionPanel(data_base_table, ExpansionOptionsElement)
			element.content.binding(self.path_manager)
			self.add_widgets(element)


class CreateEntry(CustomScrolledScreen):
	''' Базовый экран создания новой записи в базе данных '''

	def __init__(self, path_manager: PathManager, table: db.Model):
		super().__init__()

		self.name = f'create_{table.__tablename__}'.lower()
		self.path_manager = path_manager
		self.table = table

		self.setup()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate(f'Create {self.table.__tablename__}')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())


class EditEntryList(CustomScrolledScreen):
	''' Базовый класс со списком редактируемых элементов базы данных '''

	def __init__(self, path_manager: PathManager, table: db.Model):
		super().__init__()

		self.name = f'edit_{table.__tablename__}_list'.lower()
		self.path_manager = path_manager
		self.table = table

		self.setup()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate(f'Edit {self.table.__tablename__} list')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())


class Application(MDApp):
	''' Главный класс приложения '''

	def __init__(self):
		super().__init__()

		self.screen_manager = ScreenManager()
		self.path_manager = PathManager(self.screen_manager)

		self.setup()

		self.screen_manager.current = 'options'

	def setup(self) -> None:
		self.main_page = MainPage(self.path_manager)
		self.current_calls = CurrentCalls(self.path_manager)
		self.options = Options(self.path_manager)

		self.create_tag = CreateEntry(self.path_manager, Tag)
		self.create_rank = CreateEntry(self.path_manager, Rank)
		self.create_position = CreateEntry(self.path_manager, Position)
		self.create_human = CreateEntry(self.path_manager, Human)
		self.create_emergency = CreateEntry(self.path_manager, Emergency)

		self.edit_tag_list = EditEntryList(self.path_manager, Tag)
		self.edit_rank_list = EditEntryList(self.path_manager, Rank)
		self.edit_position_list = EditEntryList(self.path_manager, Position)
		self.edit_human_list = EditEntryList(self.path_manager, Human)
		self.edit_emergency_list = EditEntryList(self.path_manager, Emergency)

		self.screen_manager.add_widget(self.main_page)
		self.screen_manager.add_widget(self.current_calls)
		self.screen_manager.add_widget(self.options)

		self.screen_manager.add_widget(self.create_tag)
		self.screen_manager.add_widget(self.create_rank)
		self.screen_manager.add_widget(self.create_position)
		self.screen_manager.add_widget(self.create_human)
		self.screen_manager.add_widget(self.create_emergency)

		self.screen_manager.add_widget(self.edit_tag_list)
		self.screen_manager.add_widget(self.edit_rank_list)
		self.screen_manager.add_widget(self.edit_position_list)
		self.screen_manager.add_widget(self.edit_human_list)
		self.screen_manager.add_widget(self.edit_emergency_list)

	def build(self) -> ScreenManager:
		return self.screen_manager


def main():
	app = Application()
	app.run()


if __name__ == '__main__':
	main()