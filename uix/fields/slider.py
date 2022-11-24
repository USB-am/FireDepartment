import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import FIELDS_KV_DIR, LOCALIZED, HELP_MODE
from uix.help_button import HelpButton


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'slider.kv')
Builder.load_file(path_to_kv_file)


class FDSlider(MDBoxLayout):
	''' Виджет с полосой '''

	def __init__(self, icon: str, title: str, help_text: str=None):
		self.icon = icon
		self.title = title
		self.display_text = LOCALIZED.translate(title)

		super().__init__()

		if help_text is not None and HELP_MODE:
			self.ids.label.add_widget(HelpButton(
				title=self.__class__.__name__,
				text=help_text
			))

	def get_value(self) -> float:
		return self.current_value / 100

	def set_value(self, value: float) -> None:
		self.ids.slider.value = int(value * 100)