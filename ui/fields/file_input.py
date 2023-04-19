import os

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager

from data_base import db, ColorTheme
from config.paths import FILE_INPUT_FIELD, STATIC_DIR


Builder.load_file(FILE_INPUT_FIELD)


class FDFileInput(MDBoxLayout):
	''' Поле выбора файла из файловой системы '''

	def __init__(self, icon: str, title: str):
		self.icon = icon
		self.title = title

		super().__init__()

		self.file_manager = MDFileManager(
			exit_manager=self.close_file_manager,
			select_path=self.select_path,
			preview=True
		)
		self._path = ''

	def open_file_manager(self) -> None:
		self.file_manager.show(STATIC_DIR)

	def select_path(self, path: str) -> None:
		self.close_file_manager()
		self._path = path

	def close_file_manager(self, *_) -> None:
		self.file_manager.close()

	def get_value(self) -> str:
		return self._path

	def set_value(self, path: str) -> None:
		if not os.path.exists(path):
			raise OSError(f'Не удалось найти файл "{path}"')

		self._path = path