from app.path_manager import PathManager
import data_base
from . import BaseScrolledScreen
from ui.fields.entry import FDTextInput
from ui.fields.select_list import FDSelectList
from ui.fields.submit import FDSubmit


class _BaseCreateModelScreen(BaseScrolledScreen):
	''' Базовое представление экрана создания '''

	def __init__(self, path_manager: PathManager):
		self.path_manager = path_manager

		super().__init__()

		self.__fill_toolbar()

		self.bind(on_pre_enter=lambda *e: self._fill_content())

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda e: self.path_manager.back()
		)


class CreateTagScreen(_BaseCreateModelScreen):
	''' Экран создания тега '''

	name = 'create_tag'
	table = data_base.Tag

	def _fill_content(self) -> None:
		self.title = FDTextInput(hint_text='Название')
		self.emergencies = FDSelectList(
			icon=self.table.icon,
			title='Вызовы'
		)
		self.emergencies.add(*data_base.Emergency.query.all())
		self.submit = FDSubmit(text='Создать')
		self.submit.bind_btn(
			on_release=lambda e: print('All good!')
		)

		self.add_widgets(self.title, self.emergencies, self.submit)