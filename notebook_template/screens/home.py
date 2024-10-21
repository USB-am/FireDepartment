from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

from config import HOME_KV
from widgets.notebook import FDNotebook


Builder.load_file(HOME_KV)


class HomeScreen(Screen):
	name = 'home'

	def __init__(self, **kw):
		super().__init__(**kw)

		self.notebook = FDNotebook()
		self.ids.content.add_widget(self.notebook)
