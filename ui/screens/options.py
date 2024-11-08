from typing import List

from kivymd.app import MDApp

from . import BaseScrollScreen
from app.path_manager import PathManager
from ui.field.button import FDButtonDropdown
from ui.field.switch import FDDoubleSwitch
from ui.field.input import FDNumberInput, FDMultilineInput
from ui.field.label import FDTitle
# from config import ITERABLE_COUNT


class OptionsScreen(BaseScrollScreen):
	''' Страница с настройками '''

	name = 'options'
	toolbar_title = 'Настройки'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.__app = MDApp.get_running_app()

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)
		self.ids.toolbar.add_right_button(
			icon='check',
			callback=lambda *_: self.save_changes()
		)

		self.bind(on_pre_enter=lambda *_: self.fill_elements())

	@property
	def __theme_cls(self):
		return self.__app.theme_cls

	@property
	def __config(self):
		return self.__app.config

	def save_changes(self) -> None:
		''' Сохранить настройки в application.ini '''

		self.__save_colors_to_config()
		# try:
		# 	ITERABLE_COUNT = int(self.iterable_count_field.text)
		# except ValueError:
		# 	pass

		self._path_manager.back()

	def fill_elements(self) -> None:
		self.clear_content()

		# Название раздела
		theme_lbl = FDTitle(title='Тема')

		# Основной цвет
		self.primary_field = FDButtonDropdown(
			icon='palette',
			title='Основной цвет',
		)
		primary_field_elements = self._gen_primary_field_elements()
		self.primary_field.update_elements(primary_field_elements)

		# clr = self.__theme_cls.primary_color
		# clr = list(map(lambda c: hex(int(c*255)), clr[:-1]))
		# print(clr)
		self.primary_field.ids.btn.md_bg_color = self.__theme_cls.primary_color

		# Акцентирующий цвет
		self.accent_field = FDButtonDropdown(
			icon='palette-advanced',
			title='Акцентирующий цвет'
		)
		self.accent_field.update_elements(self._gen_accent_field_elements())
		self.accent_field.ids.btn.md_bg_color = self.__theme_cls.accent_color

		# Контрастность
		self.hue_field = FDButtonDropdown(
			icon='opacity',
			title='Контрастность',
		)
		self.hue_field.update_elements(self._gen_hue_field_elements())

		# Тема
		self.theme_style_field = FDDoubleSwitch(
			icon_active='moon-waning-crescent',
			title_active='Темная тема',
			icon_deactive='white-balance-sunny',
			title_deactive='Светлая тема',
		)
		self.theme_style_field.ids.switch.bind(on_release=lambda *_: \
			self._update_style_field(self.theme_style_field.ids.switch.active)
		)
		self.theme_style_field.set_value(self.__theme_cls.theme_style=='Dark')


		# Название раздела
		calls_lbl = FDTitle(title='Вызовы')

		# Игнорировать показатель "Рабочий день"
		self.work_day_ignore_field = FDDoubleSwitch(
			icon_active='cancel',
			title_active='Игнорировать рабочие дни',
			icon_deactive='check',
			title_deactive='В соответствии с графиком')

		# Текст начала выезда
		self.start_call_text_field = FDMultilineInput(hint_text='Начало выезда')
		self.start_call_text_field.helper_text = 'Будет вставлен при каждом начале выезда'
		self.start_call_text_field.helper_text_mode = 'on_focus'

		# Текст окончания выезда
		self.finish_call_text_field = FDMultilineInput(hint_text='Окончание выезда')
		self.finish_call_text_field.helper_text = 'Будет вставлен при окончании выезда'
		self.finish_call_text_field.helper_text_mode = 'on_focus'

		# Текст при удачном вызове человека
		self.human_call_success_field = FDMultilineInput(hint_text='Успешный вызов')
		self.human_call_success_field.helper_text = 'Будет вставлен при успешном вызове человека'
		self.human_call_success_field.helper_text_mode = 'on_focus'

		# Текст при неудачном вызове человека
		self.human_call_unsuccess_field = FDMultilineInput(hint_text='Безуспешный вызов')
		self.human_call_unsuccess_field.helper_text = 'Будет вставлен при безуспешном вызове человека'
		self.human_call_unsuccess_field.helper_text_mode = 'on_focus'

		# Количество подгружаемых элементов в пагинаторе
		# self.iterable_count_field = FDNumberInput(
		# 	hint_text='Элементы на странице',
		# 	helper_text='Увеличение значения может замедлить работу приложения!'
		# )
		# self.iterable_count_field.set_value(ITERABLE_COUNT)
		# self.iterable_count_field.bind(on_text_validate=lambda *_: print(_))

		self.add_content(theme_lbl)
		self.add_content(self.primary_field)
		self.add_content(self.accent_field)
		self.add_content(self.hue_field)
		self.add_content(self.theme_style_field)
		# self.add_content(self.iterable_count_field)

		self.add_content(calls_lbl)
		self.add_content(self.work_day_ignore_field)
		self.add_content(self.start_call_text_field)
		self.add_content(self.finish_call_text_field)
		self.add_content(self.human_call_success_field)
		self.add_content(self.human_call_unsuccess_field)

	def _gen_primary_field_elements(self) -> List:
		''' Возвращает элементы для поля primary '''

		colors = self.__theme_cls.colors.copy()
		del colors['Light']
		del colors['Dark']

		return [{
				'text': elem,
				'viewclass': 'OneLineListItem',
				'bg_color': self.__theme_cls.colors[elem][self.__theme_cls.primary_hue],
				'on_release': lambda elem=elem: self._update_primary_field(elem)
			} for elem in colors
		]

	def _gen_accent_field_elements(self) -> List:
		''' Возвращает элементы для поля accent '''

		colors = self.__theme_cls.colors.copy()
		del colors['Light']
		del colors['Dark']

		return [{
				'text': elem,
				'viewclass': 'OneLineListItem',
				'bg_color': self.__theme_cls.colors[elem][self.__theme_cls.primary_hue],
				'on_release': lambda elem=elem: self._update_accent_field(elem)
			} for elem in colors
		]

	def _gen_hue_field_elements(self) -> List:
		''' Возвращает элементы для поля hue_field '''

		return [{
				'text': elem,
				'viewclass': 'OneLineListItem',
				'bg_color': self.__theme_cls.colors[self.__theme_cls.primary_palette][elem],
				'on_release': lambda elem=elem: self._update_hue_field(elem),
			} for elem in self.__theme_cls.colors[self.__theme_cls.primary_palette].keys()
		]

	def __save_colors_to_config(self) -> None:
		config = self.__config

		config.setall('options', {
			'primary_palette': self.__theme_cls.primary_palette,
			'accent_palette': self.__theme_cls.accent_palette,
			'theme_style': self.__theme_cls.theme_style,
			'primary_hue': self.__theme_cls.primary_hue,
		})
		# config.setall('global', {
		# 	'iterable_count': self.iterable_count_field.text,
		# })
		config.write()

	def _update_primary_field(self, element: str) -> None:
		self.primary_field.ids.btn.text = element
		self.primary_field.update_elements(self._gen_primary_field_elements())
		self.primary_field.dropdown.dismiss()

		self.__theme_cls.primary_palette = element
		self.__save_colors_to_config()

	def _update_accent_field(self, element: str) -> None:
		self.accent_field.ids.btn.text = element
		self.accent_field.update_elements(self._gen_accent_field_elements())
		self.accent_field.dropdown.dismiss()

		self.__theme_cls.accent_palette = element
		self.__save_colors_to_config()

	def _update_hue_field(self, element: str) -> None:
		self.hue_field.ids.btn.text = element
		self.hue_field.update_elements(self._gen_hue_field_elements())
		self.hue_field.dropdown.dismiss()

		self.__theme_cls.primary_hue = element
		self.__save_colors_to_config()

	def _update_style_field(self, type_: bool) -> None:
		self.__theme_cls.theme_style = 'Dark' if type_ else 'Light'
		self.__save_colors_to_config()
