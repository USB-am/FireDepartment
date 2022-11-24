import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager

from config import FIELDS_KV_DIR, BASE_DIR, LOCALIZED, HELP_MODE
from uix.help_button import HelpButton


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'file_manager.kv')
Builder.load_file(path_to_kv_file)


class FileManager(MDBoxLayout):
	''' Виджет с открытием файлового менеджера '''

	def __init__(self, title: str, path: str, help_text: str=None, **options):
		self.title = title
		self.display_text = LOCALIZED.translate(title)
		self.path = path
		self.display_path = LOCALIZED.translate('File')

		super().__init__()

		self._value = ''
		self.manager = MDFileManager(
			exit_manager=lambda e: self.close(),
			**options
		)

		if help_text is not None and HELP_MODE:
			self.ids.label.add_widget(HelpButton(
				title=self.__class__.__name__,
				text=help_text
			))

		self.ids.button.bind(on_release=lambda e: self.open())

	def open(self) -> None:
		try:
			self.manager.show(self.path)
		except Exception as e:
			try:
				self.manager.show(BASE_DIR)
			except Exception as e:
				print(e)

	def close(self) -> None:
		print(f'FileManager.close() is started')
		self.manager.close()

	def set_value(self, value: str) -> None:
		self._value = value

	def get_value(self) -> str:
		if self._value is None or self._value == '':
			return None

		return self._value

	def close_dialog(self) -> None:
		self.manager.close()