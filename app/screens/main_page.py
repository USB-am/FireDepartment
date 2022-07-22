from os import path

from kivy.lang import Builder

from config import SCREENS_DIR, LOCALIZED, path_manager
from app.tools import CustomScreen


from app.tools.fields.controllers import FDSwitch
from app.tools.fields.label import *
from kivy.uix.button import Button


path_to_kv_file = path.join(SCREENS_DIR, 'main_page.kv')
Builder.load_file(path_to_kv_file)


class MainPage(CustomScreen):
	name = 'main_page'

	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('fire-truck', lambda e: print(
			path_manager.PathManager().current))

		# self.main_layout.ids.content.add_widget(FDSwitch('Content'))
		self.add_widgets(FDSwitch('Content'), FDSwitch('Human'))