import os

from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget

from app.path_manager import PathManager
from config import paths
from ui.widgets.toolbar import FDToolbar


path_to_kv_file = os.path.join(paths.BASE_SCREEN)
Builder.load_file(path_to_kv_file)


class BaseScreen(Screen):
	''' Базовый экран '''

	color = (1, 1, 1, 1)
	bg_image = None

	def __init__(self):
		super().__init__()

		self.toolbar = FDToolbar(self.name)
		self.add_widgets(self.toolbar)

	def add_widgets(self, *widgets: Widget) -> None:
		'''
		Добавляет виджеты на экран.
		~params:
		: *widgets: Widget
		'''

		[self.ids.widgets.add_widget(widget) for widget in widgets]


class BaseScrolledScreen(BaseScreen):
	''' Бозовый экран с прокрутной '''