from os import path

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from config import FIELDS_DIR, LOCALIZED


path_to_kv_file = path.join(FIELDS_DIR, 'label.kv')
Builder.load_file(path_to_kv_file)


class FDLabel(MDBoxLayout):
	def __init__(self, title: str, content: str):
		self.title = title
		self.content = content
		self.display_title = LOCALIZED.translate(title)
		self.display_content = LOCALIZED.translate(content)

		super().__init__()


class FDIcon(MDBoxLayout):
	def __init__(self, icon: str, content: str):
		self.icon = icon
		self.content = content
		self.display_content = LOCALIZED.translate(content)

		super().__init__()


class FDEntry(MDTextField):
	def __init__(self, title: str):
		self.title = title
		self.display_title = LOCALIZED.translate(title)

		super().__init__()


class FDTextArea(MDTextField):
	def __init__(self, title: str):
		self.title = title
		self.display_title = LOCALIZED.translate(title)

		super().__init__()

	def get_value(self) -> str:
		return self.text

	def set_value(self, value: str) -> None:
		self.text = value
		# super().insert_text(value)