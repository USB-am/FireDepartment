from app.path_manager import PathManager
from .base_screen import BaseScreen
from data_base import Emergency


class ModelEdit(BaseScreen):
	''' Базовый класс редактирования созданной модели '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda *_: self.path_manager.back()
		)


class EmergencyEdit(ModelEdit):
	''' Редактирование модели Emergency '''

	name = 'emergency_edit'
	toolbar_title = 'Редактирование'

	def show_fields(self) -> None:
		pass

	def _fill_content(self, emergency: Emergency) -> None:
		pass
