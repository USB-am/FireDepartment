import os.path
from typing import Union

from kivy.properties import ListProperty, BooleanProperty
from kivymd.uix.filemanager import MDFileManager

from ui.fields.button import FDIconLabelButton

from config.paths import __STATIC_DIR


_PATH = __STATIC_DIR


class FDFileInput(FDIconLabelButton):
	''' Поле с выбором файла '''

	preview = BooleanProperty(False)
	ext = ListProperty()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.path = None
		self.file_manager = None
		self.ids.button.bind(on_release=self.open_file_manager)

	def open_file_manager(self, *_) -> None:
		if self.file_manager is None:
			self.file_manager = MDFileManager(
				exit_manager=self.exit_file_manager,
				select_path=self.select_path,
				preview=self.preview,
				ext=self.ext
			)

		self.file_manager.show(_PATH)

	def exit_file_manager(self, *_) -> None:
		if self.file_manager is not None:
			self.file_manager.close()

		self.set_value(None)

	def select_path(self, path) -> None:
		if os.path.isfile(path):
			self.set_value(path)

		self.file_manager.close()

	def get_value(self) -> Union[str, None]:
		return self.path

	def set_value(self, path: Union[str, None]) -> None:
		self.ids.button.text = self.button_text if path is None else os.path.basename(path)
		self.path = path