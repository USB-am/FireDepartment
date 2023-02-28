from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

from config import paths


Builder.load_file(paths.BOTTOM_NAVIGATION_WIDGET)


class FDBottomNavigation(MDBoxLayout):
	''' Навигация внизу экрана '''

	def add_items(self, *items: MDBottomNavigationItem) -> None:
		container = self.ids.nav
		[container.add_widget(item) for item in items]