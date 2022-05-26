# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager

from config import BASE_DIR, PATTERNS_DIR, LOCALIZED
from data_base import db, ColorTheme


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'file_manager_field.kv')
Builder.load_file(path_to_kv_file)


def check_image_input_valid(func):
	correct_types = ('.jpeg', '.jpg', '.png')

	def wrapper(instance, path) -> func:
		ext = os.path.splitext(path)[1]

		file_is_exists = os.path.exists(path)
		type_is_correct = ext in correct_types

		if not file_is_exists:
			raise OSError(f'File {path} is not exists!')
		if not type_is_correct:
			raise AttributeError(f'File {path} is not correct!')

		return func(instance, path)

	return wrapper


class FileManagerField(MDBoxLayout):
	icon = 'image-size-select-actual'

	def __init__(self, title: str, *_):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)

		super().__init__()

		self.file_manager = MDFileManager(
			exit_manager=self.exit_manager,
			select_path=self.select_path,
		)
		self._value = None

	def open(self) -> None:
		self.file_manager.show(BASE_DIR)

	def exit_manager(self, *_) -> None:
		self.file_manager.close()

	@check_image_input_valid
	def select_path(self, path: str) -> None:
		ColorTheme.query.all()[0].background_image = path
		print(ColorTheme.query.all()[0].background_image)
		db.session.commit()
		self.file_manager.close()
		self._value = path

	def get_value(self) -> str:
		return self._value

	def set_value(self, value: str) -> None:
		self._value = value