from typing import Any, List

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

from .base import BaseScrollScreen
from app.path_manager import PathManager
from ui.field.button import FDButtonDropdown
from ui.field.switch import FDDoubleSwitch
from ui.field.input import FDNumberInput, FDMultilineInput
from ui.field.label import FDTitle


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

	def __get_config_value(self, section: str, option: str, fallback: Any='') -> Any:
		'''
		Получить значение из конфига.

		~params:
		section: str - секция конфига в которой будет идти поиск значения;
		option: str - ключ по которому будет возвращено значение;
		fallback: Any - значение при ненахождении (не может быть None).
		'''
		return self.__config.get(section, option, fallback=fallback)

	def save_changes(self) -> None:
		''' Сохранить настройки в application.ini '''

		self.__save_to_config()
		self._path_manager.forward('main')

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
		self.work_day_ignore_field.set_value(bool(
			self.__get_config_value(
				section='call',
				option='work_day_ignore',
				fallback='1'
			)))
		work_day_ignore_info = MDLabel(
			text='[b]Примечание[/b]:\n' + \
				'[i]Если [b]включено[/b], при начале выезда будут добавлены все сотрудники связанные с этим выездом.[/i]\n' + \
				'[i]Если [b]выключено[/b], выбраны будут только сотрудники работающие в настоящее время (в соответствии с рабочим графиком).[/i]\n',
			adaptive_height=True,
			markup=True,
			theme_text_color='Hint'
		)

		# Текст начала выезда
		self.start_call_text_field = FDMultilineInput(hint_text='Начало выезда')
		self.start_call_text_field.helper_text = 'Будет вставлен при каждом начале выезда'
		self.start_call_text_field.helper_text_mode = 'persistent'
		self.start_call_text_field.current_hint_text_color = self.__theme_cls.text_color
		self.start_call_text_field.set_value(
			self.__get_config_value(
				section='call',
				option='start_text',
				fallback='[HH:MM dd.mm.yyyy] Начало выезда.'
			))

		# Текст окончания выезда
		self.finish_call_text_field = FDMultilineInput(hint_text='Окончание выезда')
		self.finish_call_text_field.helper_text = 'Будет вставлен при окончании выезда'
		self.finish_call_text_field.helper_text_mode = 'persistent'
		self.finish_call_text_field.current_hint_text_color = self.__theme_cls.text_color
		self.finish_call_text_field.set_value(
			self.__get_config_value(
				section='call',
				option='finish_text',
				fallback='[HH:MM dd.mm.yyyy] Конец выезда.'
			))

		# Текст при удачном вызове человека
		self.human_call_success_field = FDMultilineInput(hint_text='Успешный вызов')
		self.human_call_success_field.helper_text = 'Будет вставлен при успешном вызове человека'
		self.human_call_success_field.helper_text_mode = 'persistent'
		self.human_call_success_field.current_hint_text_color = self.__theme_cls.text_color
		self.human_call_success_field.set_value(
			self.__get_config_value(
				section='call',
				option='human_success',
				fallback='[HH:MM dd.mm.yyyy] Вызов {human_name}.'
			))

		# Текст при неудачном вызове человека
		self.human_call_unsuccess_field = FDMultilineInput(hint_text='Безуспешный вызов')
		self.human_call_unsuccess_field.helper_text = 'Будет вставлен при безуспешном вызове человека'
		self.human_call_unsuccess_field.helper_text_mode = 'persistent'
		self.human_call_unsuccess_field.current_hint_text_color = self.__theme_cls.text_color
		self.human_call_unsuccess_field.set_value(
			self.__get_config_value(
				section='call',
				option='human_unsuccess',
				fallback='[HH:MM dd.mm.yyyy] Вызов {human_name} не прошел.'
			))

		call_text_info = MDLabel(
			text='[b]Примечание:[/b]\n' + \
				'[i]В поля "Успешный вызов" и "Безуспешный вызов" можно добавить:\n' + \
				'- {human_name} для вставки ФИО сотрудника;\n' + \
				'- {human_phone_1} для вставки основного номера телефона;\n' + \
				'- {human_phone_2} для вставки дополнительного номера телефона.\n',
			adaptive_height=True,
			markup=True,
			theme_text_color='Hint'
		)

		# Добавление настроек темы
		self.add_content(theme_lbl)
		self.add_content(self.primary_field)
		self.add_content(self.accent_field)
		self.add_content(self.hue_field)
		self.add_content(self.theme_style_field)

		# Добавление настроек вызовов
		self.add_content(calls_lbl)
		self.add_content(self.work_day_ignore_field)
		self.add_content(work_day_ignore_info)
		self.add_content(self.start_call_text_field)
		self.add_content(self.finish_call_text_field)
		self.add_content(self.human_call_success_field)
		self.add_content(self.human_call_unsuccess_field)
		self.add_content(call_text_info)

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

	def __save_to_config(self) -> None:
		config = self.__config

		config.setall(
			'options', {
				'primary_palette': self.__theme_cls.primary_palette,
				'accent_palette': self.__theme_cls.accent_palette,
				'theme_style': self.__theme_cls.theme_style,
				'primary_hue': self.__theme_cls.primary_hue,
			}
		)
		config.setall(
			'call', {
				'work_day_ignore': '1' if self.work_day_ignore_field.get_value() else '',
				'start_text': self.start_call_text_field.get_value(),
				'finish_text': self.finish_call_text_field.get_value(),
				'human_success': self.human_call_success_field.get_value(),
				'human_unsuccess': self.human_call_unsuccess_field.get_value(),
			}
		)
		config.write()

	def _update_primary_field(self, element: str) -> None:
		self.primary_field.ids.btn.text = element
		self.primary_field.update_elements(self._gen_primary_field_elements())
		self.primary_field.dropdown.dismiss()

		self.__theme_cls.primary_palette = element
		self.__save_to_config()

	def _update_accent_field(self, element: str) -> None:
		self.accent_field.ids.btn.text = element
		self.accent_field.update_elements(self._gen_accent_field_elements())
		self.accent_field.dropdown.dismiss()

		self.__theme_cls.accent_palette = element
		self.__save_to_config()

	def _update_hue_field(self, element: str) -> None:
		self.hue_field.ids.btn.text = element
		self.hue_field.update_elements(self._gen_hue_field_elements())
		self.hue_field.dropdown.dismiss()

		self.__theme_cls.primary_hue = element
		self.__save_to_config()

	def _update_style_field(self, type_: bool) -> None:
		self.__theme_cls.theme_style = 'Dark' if type_ else 'Light'
		self.__save_to_config()
