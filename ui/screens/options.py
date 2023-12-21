from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.picker import MDThemePicker

from . import BaseScrollScreen
from app.path_manager import PathManager
from ui.field.button import FDButton
from config import CONF


class OptionsScreen(BaseScrollScreen):
	''' Страница с настройками '''

	name = 'options'
	toolbar_title = 'Настройки'
	config = None	# Обновляется в методе build класса App

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)

		self.fill_elements()

	def fill_elements(self) -> None:
		self.color_theme = FDButton(
			icon='palette',
			title='Цветовая схема',
			btn_text='Выбрать'
		)
		self.color_theme.ids.btn.bind(on_release=lambda *_: self._open_theme_picker())

		self.add_content(self.color_theme)

	def _open_theme_picker(self) -> None:
		''' Открыть диалоговое окно выбора темы '''

		dialog = MDThemePicker(on_pre_dismiss=lambda *_: self.__save_colors_to_config())
		dialog.open()

	def __save_colors_to_config(self) -> None:
		if self.config is None:
			return

		app = MDApp.get_running_app()
		config = app.config
		theme_cls = app.theme_cls

		config.setall('options', {
			'primary_palette': theme_cls.primary_palette,
			'accent_palette': theme_cls.accent_palette,
			'theme_style': theme_cls.theme_style,
		})
		config.write()
