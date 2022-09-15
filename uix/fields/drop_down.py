import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import LOCALIZED, FIELDS_KV_DIR


path_to_kv_path = os.path.join(FIELDS_KV_DIR, 'drop_down.kv')
Builder.load_file(path_to_kv_file)


class DropDown(MDBoxLayout):
	def __init__(self, icon: str, title: str):
		self.icon = icon
		self.title = title
		self.display_text = LOCALIZED.translate(title)

		super().__init__()