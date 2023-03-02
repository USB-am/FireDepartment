from kivy.lang.builder import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

from config import paths


from kivymd.uix.label import MDLabel


Builder.load_file(paths.BOTTOM_NAVIGATION_ITEMS)


class EmergenciesNavigationItem(MDBottomNavigationItem):
	''' Ячейка с списком выездов '''

	def __init__(self, **options):
		super().__init__(**options)

		[self.ids.content.add_widget(MDLabel(text=f'Row #{i+1}')) \
			for i in range(100)]