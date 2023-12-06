from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base import db, Tag
from ui.field.input import FDInput


class _BaseCreateModel(BaseScrollScreen):
	''' Базовое представление страницы создания записи в БД '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda *_: self._path_manager.back()
		)
		self.ids.toolbar.add_right_button(
			icon='check',
			callback=lambda *_: print('Save button is pressed!')
		)

		self.fill_elements()

	def fill_elements(self) -> None:
		pass


class TagCreateModel(_BaseCreateModel):
	''' Страница создания модели Tag '''

	name = 'create_tag'
	model = Tag
	toolbar_title = 'Создание Тега'

	def fill_elements(self) -> None:
		self.title_field = FDInput(hint_text='Название')
		self.add_content(self.title_field)
