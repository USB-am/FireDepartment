from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRectangleFlatIconButton

from custom_screen import CustomScrolledScreen
from config import LOCALIZED
from uix import fields
from data_base import UserSettings
from data_base import manager as DBManager


class CustomButton(MDFloatLayout):
	''' Кнопка для открытия окна кастомизации '''
	def __init__(self, **options):
		super().__init__(
			size_hint=(1, None),
			size=(self.width, 50)
		)

		self.button = MDRectangleFlatIconButton(
			pos_hint={'center_x': .5, 'center_y': .5},
			**options
		)
		self.add_widget(self.button)


class GlobalOptions(CustomScrolledScreen):
	''' Экран дополнительных общих настроек '''

	name = 'global_options'

	def __init__(self, path_manager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Global')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())

	def fill_content(self) -> None:
		self.help_mode = fields.BooleanField(
			icon='chat-question',
			title='Off/On hints',
			help_text='Выключить/Включить подсказки'
		)
		self.help_mode.ids.switch.bind(on_release=lambda e: self._update_help_mode())

		language_items = [
			{
				'text': 'RU',
				'viewclass': 'OneLineListItem',
				'on_release': lambda e='ru': self._update_language(e)
			}, {
				'text': 'EN',
				'viewclass': 'OneLineListItem',
				'on_release': lambda e='en': self._update_language(e)
			}
		]
		self.language = fields.DropDown(
			icon='translate',
			title='Language',
			help_text='Выбор языка'
		)
		self.language.add(language_items)

		self.custom_screen_button = CustomButton(
			text=LOCALIZED.translate('Customization')
		)
		self.custom_screen_button.button.bind(on_release=lambda e: \
			self.path_manager.forward('edit_colortheme'))

		self.add_widgets(self.help_mode)
		self.add_widgets(self.language)
		self.add_widgets(self.custom_screen_button)

	def _update_help_mode(self) -> None:
		entry = UserSettings.query.first()
		values = {'help_mode': self.help_mode.get_value()}

		DBManager.update(entry, values)

	def _update_language(self, lang: str) -> None:
		entry = UserSettings.query.first()
		values = {'language': lang.lower()}

		DBManager.update(entry, values)