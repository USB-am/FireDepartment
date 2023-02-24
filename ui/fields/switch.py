from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import paths


Builder.load_file(paths.SWITCH_FIELD)


class FDSwitch(MDBoxLayout):
	''' Переключатель '''

	icon = StringProperty()
	title = StringProperty()

	def get_value(self) -> bool:
		return self.ids.switch.active

	def set_value(self, value: bool) -> None:
		self.ids.switch.active = value