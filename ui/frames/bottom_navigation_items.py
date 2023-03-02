from kivy.lang.builder import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

from config import paths
from .list_items import FDEmergencyListItem
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

		for emergency in emergencies:
			container.add_widget(FDEmergencyListItem(model=emergency))