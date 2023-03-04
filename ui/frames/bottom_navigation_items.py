from kivy.lang.builder import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

from config import paths
from .list_items import FDEmergencyListItem, FDHumanListItem
import data_base


Builder.load_file(paths.BOTTOM_NAVIGATION_ITEMS)


class EmergenciesNavigationItem(MDBottomNavigationItem):
	''' Ячейка с списком выездов '''

	def __init__(self, **options):
		super().__init__(**options)

		self.__fill_content()

	def __fill_content(self) -> None:
		emergencies = data_base.Emergency.query.all()

		self.add_list_items(*emergencies)

	def add_list_items(self, *emergencies: data_base.Emergency) -> None:
		container = self.ids.content

		[container.add_widget(FDEmergencyListItem(model=emergency)) \
			for emergency in emergencies]


class ContactsNavigationItem(MDBottomNavigationItem):
	''' Ячейка с списком контактов '''

	def __init__(self, **options):
		super().__init__(**options)

		self.__fill_content()

	def __fill_content(self) -> None:
		humans = data_base.Human.query.filter(data_base.Human.is_firefigher==True)

		self.add_list_items(*humans)

	def add_list_items(self, *humans: data_base.Human) -> None:
		container = self.ids.content

		[container.add_widget(FDHumanListItem(model=human)) \
			for human in humans]