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
from data_base import db, Tag, Rank, Position, Emergency


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
		print(f'CurrentCalls.add_tab accept element={element.title}')
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
		for data_base_table in (Tag, Rank, Position, Emergency):
			element = FDExpansionPanel(data_base_table, ExpansionOptionsElement)
			element.content.binding(self.path_manager)
			self.add_widgets(element)


class Application(MDApp):
	''' Главный класс приложения '''

	def __init__(self):
		super().__init__()

		self.screen_manager = ScreenManager()
		self.path_manager = PathManager(self.screen_manager)

		self.setup()

		self.screen_manager.current = 'main_page'

	def setup(self) -> None:
		self.main_page = MainPage(self.path_manager)
		self.options = Options(self.path_manager)
		self.current_calls = CurrentCalls(self.path_manager)

		self.screen_manager.add_widget(self.main_page)
		self.screen_manager.add_widget(self.options)
		self.screen_manager.add_widget(self.current_calls)

	def build(self) -> ScreenManager:
		return self.screen_manager


def main():
	app = Application()
	app.run()


if __name__ == '__main__':
	main()