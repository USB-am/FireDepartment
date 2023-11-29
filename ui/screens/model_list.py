from typing import Type

from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base import db, Tag
from ui.layout.model_list_element import ModelListElement


__all__ = ('TagsList',)


class _ModelList(BaseScrollScreen):
	''' Базовый класс с элементами из базы данных '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)
		self.ids.toolbar.add_right_button(
			icon='file-plus',
			callback=None
		)

		self.fill_elements()

	def fill_elements(self) -> None:
		pass


class TagsList(_ModelList):
	''' Класс с элементами из модели Tag '''

	name = 'tags_list'
	model = Tag
	toolbar_title = 'Теги'

	def fill_elements(self) -> None:
		for tag in self.model.query.all():
			list_elem = ModelListElement(entry=tag, icon=Tag.icon)
			list_elem.bind_edit_btn(lambda t=tag: print(f'Edit btn {t.title}'))
			list_elem.bind_info_btn(lambda t=tag: print(f'Info btn {t.title}'))
			self.add_content(list_elem)
