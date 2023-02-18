import os

from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget

from app.path_manager import PathManager
from config import paths


path_to_kv_file = os.path.join(paths.BASE_SCREEN)
Builder.load_file(path_to_kv_file)


class BaseScreen(Screen):
	''' Базовый экран '''

	def __init__(self):
		super().__init__()

	def add_widgets(self, *widgets: Widget) -> None:
		'''
		Добавляет виджеты на экран.
		~params:
		: *widgets: Widget
		'''

		[self.ids.widgets.add_widget(widget) for widget in widgets]


class BaseScrolledScreen(BaseScreen):
	''' Бозовый экран с прокрутной '''