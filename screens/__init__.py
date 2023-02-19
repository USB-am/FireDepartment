import os

from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget

from app.path_manager import PathManager
from config import paths
from ui.widgets.toolbar import FDToolbar
from ui.frames.scrolled import FDScrolledFrame


path_to_kv_file = os.path.join(paths.BASE_SCREEN)
Builder.load_file(path_to_kv_file)


class BaseScreen(Screen):
	''' Базовый экран '''

	color = (1, 1, 1, 1)
	bg_image = None

	def __init__(self):
		super().__init__()

		self.toolbar = FDToolbar(self.name)
		self.ids.widgets.add_widget(self.toolbar)

	def add_widgets(self, *widgets: Widget) -> None:
		'''
		Добавляет виджеты на экран.
		~params:
		: *widgets: Widget
		'''

		[self.ids.widgets.add_widget(widget) for widget in widgets]


class BaseScrolledScreen(BaseScreen):
	''' Бозовый экран с прокрутной '''

	def __init__(self, *pre_scroll_widgets: Widget):
		super().__init__()

		for widget in pre_scroll_widgets:
			self.ids.widgets.add_widget(widget)

		self.scrolled_frame = FDScrolledFrame()
		self.ids.widgets.add_widget(self.scrolled_frame)

	def add_widgets(self, *widgets: Widget) -> None:
		self.scrolled_frame.add_widgets(*widgets)

	def clear(self) -> None:
		container = self.scrolled_frame.ids.content
		container.clear_widgets()