from kivy.metrics import dp

from . import BaseScrolledScreen
from app.path_manager import PathManager
from data_base import ColorTheme
from ui.fields.file_input import FDFileInput
from ui.fields.submit import FDSubmit
from ui.fields.colors import FDColor


class EditColorTheme(BaseScrolledScreen):
	''' Экран кастомизации '''

	name = 'color_theme_edit'
	table = ColorTheme

	def __init__(self, path_manager: PathManager):
		super().__init__()
		self.scrolled_frame.ids.content.spacing = dp(10)

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
		self.bg_color = FDColor(
			icon='flip-to-back',
			title='Цвет заднего фона'
		)

		self.submit = FDSubmit(text='Изменить')
		self.submit.bind_btn(
			callback=lambda e: self.update_theme()
		)

		self.add_widgets(self.file_input, self.bg_color, self.submit)

	def update_theme(self) -> None:
		self.bg_image = self.file_input.get_value()

		self.reboot_bg_image(source=self.bg_image)
		print(self.bg_image)