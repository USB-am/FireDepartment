from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from config import BASE_SCREEN
from ui.widgets.toolbar import FDToolbar


Builder.load_file(BASE_SCREEN)


class BaseScreen(Screen):
	''' Базовое представление страницы (без прокрутки). '''

	def __init__(self):
		super().__init__()

	def add_content(self, widget: Widget) -> None:
		'''
		Добавляет виджет на страницу.

		~params:
		widget: Widget - любой элемент, который можно отобразить через
			метод add_widget.
		'''

		self.ids.content.add_widget(widget)

	def open_menu(self, *events) -> None:
		''' Открывает боковое меню. '''

		self.parent.parent.ids.menu.set_state('open')


class BaseScrollScreen(Screen):
	''' Базовое представление страницы (с прокруткой). '''

	def __init__(self):
		super().__init__()

	def add_content(self, widget: Widget) -> None:
		'''
		Добавляет виджет на страницу.

		~params:
		widget: Widget - любой элемент, который можно отобразить через
			метод add_widget.
		'''

		self.ids.content.add_widget(widget)

	def open_menu(self, *events) -> None:
		''' Открывает боковое меню. '''

		self.parent.parent.ids.menu.set_state('open')