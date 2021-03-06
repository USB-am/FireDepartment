from os import path

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import FIELDS_DIR, LOCALIZED


path_to_kv_file = path.join(FIELDS_DIR, 'controllers.kv')
Builder.load_file(path_to_kv_file)


class FDSwitch(MDBoxLayout):
	''' Переключатель '''
	def __init__(self, icon: str, title: str):
		self.icon = icon
		self.title = title
		self.display_title = LOCALIZED.translate(title)

		super().__init__()

	def get_value(self) -> bool:
		return self.ids.switch.active

	def set_value(self, value: bool) -> None:
		self.ids.switch.active = value