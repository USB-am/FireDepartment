import os

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivymd.uix.toolbar import MDToolbar

from uix import FDScrollFrame
from config import STATIC_DIR


path_to_kv_file = os.path.join(os.getcwd(), 'kv', 'custom_screen.kv')
Builder.load_file(path_to_kv_file)


class FDToolbar(MDToolbar):
	''' Верхняя панель '''

	def __init__(self, title: str):
		self.title = title
		self.left_buttons = []
		self.right_buttons = []

		super().__init__()

	def add_left_button(self, icon: str, callback) -> None:
		self.left_action_items.append([icon, callback])

	def add_right_button(self, icon: str, callback) -> None:
		self.right_action_items.append([icon, callback])


class CustomScreen(Screen):
	''' Базовый экран '''

	bg_image = None
	color = (1, 1, 1, .3)

	def __init__(self):
		super().__init__()

		self.toolbar = FDToolbar('Base')
		self.ids.widgets.add_widget(self.toolbar)

	def add_widgets(self, *widgets: Widget) -> None:
		[self.ids.widgets.add_widget(widget) for widget in widgets]

	def reboot_styles(self, rgba: tuple=None, source: str=None) -> None:
		if rgba is not None:
			CustomScreen.color = rgba

		if source is not None:
			CustomScreen.bg_image = source

		with self.canvas.before:
			c = Color(*CustomScreen.color)

			self.rect = Rectangle(
				size=self.size,
				pos=self.pos,
				source=CustomScreen.bg_image)


class CustomScrolledScreen(CustomScreen):
	''' Базовый экран с прокруткой '''

	def __init__(self, *pre_scroll_widgets: Widget):
		super().__init__()

		for widget in pre_scroll_widgets:
			self.ids.widgets.add_widget(widget)

		self.scrolled_frame = FDScrollFrame()
		self.ids.widgets.add_widget(self.scrolled_frame)

	def add_widgets(self, *widgets: Widget) -> None:
		self.scrolled_frame.add_widgets(*widgets)

	def clear(self) -> None:
		container = self.scrolled_frame.ids.content
		container.clear_widgets()