from custom_screen import CustomScrolledScreen
from config import LOCALIZED
from uix import fields


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
			title='Off/On hints'
		)
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
			title='Language'
		)
		self.language.add(language_items)

		self.add_widgets(self.help_mode)
		self.add_widgets(self.language)

	def _update_language(self, lang: str) -> None:
		print(f'Update language to {lang}')