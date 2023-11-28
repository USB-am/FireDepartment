from typing import Type

from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base import db, Tag


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
			icon='note-plus',
			callback=None
		)

		for model in self.model.query.all():
			print(model.title)


class TagsList(_ModelList):
	'''
	Класс с элементами из модели Tag.
	'''

	name = 'tags_list'
	model = Tag
	toolbar_title = 'Теги'
