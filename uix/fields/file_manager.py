import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager

from config import FIELDS_KV_DIR, BASE_DIR, LOCALIZED


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'file_manager.kv')
Builder.load_file(path_to_kv_file)


class FileManager(MDBoxLayout):
	''' Виджет с открытием файлового менеджера '''

	def __init__(self, title: str, path: str, **options):
		self.title = title
		self.display_text = LOCALIZED.translate(title)
		self.path = path
		self.display_path = LOCALIZED.translate('File')

		super().__init__()

		self.manager = MDFileManager(**options)

		self.ids.button.bind(on_release=lambda e: self.open())

	def open(self) -> None:
		try:
			self.manager.show(self.path)
		except Exception as e:
			try:
				self.manager.show(BASE_DIR)
			except Exception as e:
				print(e)

	def set_value(self, value: str) -> None:
		if value is None:
			value = '-'

		self.ids.button.text = value

	def get_value(self) -> str:
		return None

	def close_dialog(self) -> None:
		self.manager.close()