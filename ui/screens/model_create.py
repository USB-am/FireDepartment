from app.path_manager import PathManager
from .base_screen import BaseScreen
from data_base import Emergency
from ui.fields.contents.model_content import EmergencyModelContent


class ModelCreate(BaseScreen):
	''' Базовый класс создания модели '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda *_: self.path_manager.back()
		)


class EmergencyCreate(ModelCreate):
	''' Создание модели Emergency '''

	name = 'emergency_create'
	toolbar_title = 'Создание'
	content_cls = EmergencyModelContent
