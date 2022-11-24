import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from uix.help_button import HelpButton
from config import FIELDS_KV_DIR, LOCALIZED, HELP_MODE


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'boolean_field.kv')
Builder.load_file(path_to_kv_file)


class BooleanField(MDBoxLayout):
	''' Поле с переключателем '''

	def __init__(self, icon: str, title: str, help_text: str=None):
		self.icon = icon
		self.title = title
		self.display_text = LOCALIZED.translate(title)

		super().__init__()

		if help_text is not None and HELP_MODE:
			self.ids.label.add_widget(HelpButton(
				title=self.__class__.__name__,
				text=help_text))

	def set_value(self, value: bool) -> None:
		if value is None:
			value = False

		self.ids.switch.active = value

	def get_value(self) -> bool:
		return self.ids.switch.active