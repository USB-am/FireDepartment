# -*- coding: utf-8 -*-

# Temp import
from kivy.config import Config
# Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')


from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from app.tools.custom_screen import CustomScrolledScreen
from data_base import Emergency


from app.tools.fields.selected_list import SelectedList


class Application(MDApp):
	def __init__(self, *a, **kw):
		super().__init__(*a, **kw)
		self.main_screen = CustomScrolledScreen()
		sl = SelectedList('bus', 'Test Polygon', show_create=True)
		sl.update_content(Emergency.query.all())
		self.main_screen.add_widgets(sl)

	def build(self):
		return self.main_screen