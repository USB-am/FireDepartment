import data_base

from . import create_model


class _BaseEditModelScreen:
	''' Базовое представление экрана редактирования '''

	def fill_content(self, entry: data_base.db.Model) -> None:
		raise AttributeError('Class _BaseEditModelScreen is hasn\'t "fill_content" method!')


class EditTagScreen(_BaseEditModelScreen, create_model.CreateTagScreen):
	''' Экран редактирования тега '''

	name = 'edit_tag'
	table = data_base.Tag

	def fill_content(self, tag_entry: data_base.Tag) -> None:
		self.title.set_value(tag_entry.title)
		# print(type(tag_entry.emergencies), tag_entry.emergencies, sep='\n')