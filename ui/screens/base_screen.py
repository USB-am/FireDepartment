from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

from ui.widgets.toolbar import Toolbar
from config.paths import __BASE_SCREEN_DIR


class BaseScreen(Screen):
	color = [1, 1, 1, 1]
	bg_image = None

	def __init__(self):
		super().__init__()

		self.toolbar = Toolbar()
		self.ids.widgets.add_widget(self.toolbar)