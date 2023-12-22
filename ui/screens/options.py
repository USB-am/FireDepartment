from typing import List

from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.picker import MDThemePicker

from . import BaseScrollScreen
from app.path_manager import PathManager
from ui.field.button import FDButton, FDButtonDropdown
from config import CONF


class OptionsScreen(BaseScrollScreen):
	''' Страница с настройками '''

	name = 'options'
	toolbar_title = 'Настройки'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.__app = MDApp.get_running_app()
		# self.__theme_cls = self.__app.theme_cls

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)

		self.bind(on_pre_enter=lambda *_: self.fill_elements())

	@property
	def __theme_cls(self):
		return self.__app.theme_cls

	@property
	def __config(self):
		return self.__app.config

	def fill_elements(self) -> None:
		self.clear_content()

		self.color_theme_field = FDButton(
			icon='palette',
			title='Цветовая схема',
			btn_text='Выбрать'
		)
		self.color_theme_field.ids.btn.bind(on_release=lambda *_: self._open_theme_picker())

		self.hue_field = FDButtonDropdown(
			icon='opacity',
			title='Контрастность',
		)
		self.hue_field.update_elements(self._gen_hue_field_elements())
		self.hue_field.elems.append({'text': 'test', 'viewclass': 'OneLineListItem'})

		self.add_content(self.color_theme_field)
		self.add_content(self.hue_field)

	def _gen_hue_field_elements(self) -> List:
		''' Возвращает элементы для поля hue_field '''

		return [{
				'text': elem,
				'viewclass': 'OneLineListItem',
				'bg_color': self.__theme_cls.colors[self.__theme_cls.primary_palette][elem],
				'on_release': lambda elem=elem: self._update_hue_field(elem),
			} for elem in self.__theme_cls.colors[self.__theme_cls.primary_palette].keys()
		]

	def _open_theme_picker(self) -> None:
		''' Открыть диалоговое окно выбора темы '''

		dialog = MDThemePicker(on_pre_dismiss=lambda *_: self.__save_colors_to_config())
		dialog.open()

	def __save_colors_to_config(self) -> None:
		config = self.__config

		config.setall('options', {
			'primary_palette': self.__theme_cls.primary_palette,
			'accent_palette': self.__theme_cls.accent_palette,
			'theme_style': self.__theme_cls.theme_style,
			'primary_hue': self.__theme_cls.primary_hue,
		})
		config.write()

	def _update_hue_field(self, element) -> None:
		self.hue_field.ids.btn.text = element
		self.hue_field.update_elements(self._gen_hue_field_elements())
		self.hue_field.dropdown.dismiss()

		self.__theme_cls.primary_hue = element
		self.__save_colors_to_config()
