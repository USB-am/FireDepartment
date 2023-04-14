from . import BaseBottomNavigationScreen
from app.path_manager import PathManager

from ui.frames.bottom_navigation_items import EmergenciesNavigationItem, \
	ContactsNavigationItem


class MainScreen(BaseBottomNavigationScreen):
	''' Главная страница '''

	name = 'main'

	def __init__(self, path_manager: PathManager):
		self.path_manager = path_manager
		super().__init__()

		self.__fill()

		self.bind(on_pre_enter=lambda e: self.update_navigation_tabs())

	def update_navigation_tabs(self) -> None:
		self.emergencies_item.update()
		self.contacts_item.update()

	def __fill(self) -> None:
		self.__fill_toolbar()
		self.__fill_content()

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='fire-truck',
			callback=lambda event: print('fire-truck')
		)
		self.toolbar.add_right_button(
			icon='face-agent',
			callback=lambda event: self.path_manager.forward('options')
		)

	def __fill_content(self) -> None:
		self.emergencies_item = EmergenciesNavigationItem(
			name='emergencies_item',
			text='Вызовы',
			icon='phone-alert'
		)

		self.contacts_item = ContactsNavigationItem(
			name='contacts_item',
			text='Контакты',
			icon='card-account-phone'
		)
		self.add_widgets(self.emergencies_item, self.contacts_item)