from custom_screen import CustomScrolledScreen

from config import LOCALIZED
from uix import EmergencySearchBlock, FDExpansionPanel, ExpansionEmergencyElement


class MainPage(CustomScrolledScreen):
	''' Главный экран '''

	name = 'main_page'

	def __init__(self, path_manager):
		self.filter_ = EmergencySearchBlock()

		super().__init__(self.filter_)

		self.path_manager = path_manager

		self.setup()
		self.bind(on_pre_enter=lambda e: self.fill_content())
		self.filter_.entry.binding(self.fill_content)
		self.filter_.delete_button.bind(on_release=lambda e: self.reset_search())

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Main')
		self.toolbar.add_left_button('fire-truck',
			lambda e: self.path_manager.forward('current_calls'))
		self.toolbar.add_right_button('cog',
			lambda e: self.path_manager.forward('options'))

	def fill_content(self) -> None:
		self.clear()

		for emergency in self.filter_.filter():
			element = FDExpansionPanel(emergency, ExpansionEmergencyElement)
			self.add_widgets(element)

	def reset_search(self) -> None:
		self.filter_.entry.text = ''
		self.fill_content()