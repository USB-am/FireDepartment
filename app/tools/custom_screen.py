from os import path

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from config import TOOLS_DIR, path_manager
from app.tools.toolbar import FDToolbar
from app.tools.scroll_layout import FDScrollLayout


path_to_kv_file = path.join(TOOLS_DIR, 'custom_screen.kv')
Builder.load_file(path_to_kv_file)


class CustomScreen(Screen):
	''' Базовый экран '''
	color = (0, 0, 0, 0)
	bg_image = 'C:\\Python\\AndroidApps\\FireDepartment_Finish\\app\\images\\_bg.png'

	def __init__(self):
		super().__init__()

		self.toolbar = FDToolbar(self.name)
		self.ids.widgets.add_widget(self.toolbar)

	def forward(self, screen_name: str) -> Screen:
		return path_manager.PathManager().forward(screen_name)

	def back(self) -> Screen:
		return path_manager.PathManager().back()


class CustomScrolledScreen(CustomScreen):
	''' Экран с прокруткой '''
	def __init__(self):
		self.main_layout = FDScrollLayout()

		super().__init__()

		self.ids.widgets.add_widget(self.main_layout)

	def add_widgets(self, *widgets: Widget) -> None:
		for widget in widgets:
			self.main_layout.ids.content.add_widget(widget)

	def clear_scroll_content(self) -> None:
		content = self.main_layout.ids.content
		content.clear_widgets()