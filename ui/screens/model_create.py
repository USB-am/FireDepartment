from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base import db, Tag, Emergency
from ui.field.input import FDInput
from ui.field.button import FDRectangleButton
from ui.field.select import FDMultiSelect


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
		self.title_field = FDInput(
			hint_text='Название', required=True,
			helper_text_mode='on_error', max_text_length=25,
			helper_text='Поле не может быть пустым или неуникальным')
		self.emergencies_field = FDMultiSelect(title='Вызовы', model=Emergency)
		self.emergencies_field.bind_btn(
			lambda: self._path_manager.forward('create_emergency'
		))
		self.save_btn = FDRectangleButton(title='Сохранить')

		self.add_content(self.title_field)
		self.add_content(self.emergencies_field)
		self.add_content(self.save_btn)
