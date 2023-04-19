from . import BaseScrolledScreen
from app.path_manager import PathManager
from data_base import ColorTheme
from ui.fields.file_input import FDFileInput
from ui.fields.submit import FDSubmit


class EditColorTheme(BaseScrolledScreen):
	''' Экран кастомизации '''

	name = 'color_theme_edit'
	table = ColorTheme

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager
		self.__fill_toolbar()
		self.__fill_content()

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda e: self.path_manager.back()
		)

	def __fill_content(self) -> None:
		self.file_input = FDFileInput(
			icon='image-edit',
			title='Задний фон'
		)

		self.submit = FDSubmit(text='Изменить')
		self.submit.bind_btn(
			callback=lambda e: self.update_theme()
		)

		self.add_widgets(self.file_input, self.submit)

	def update_theme(self) -> None:
		pass