from kivy.metrics import dp
from kivy.parser import parse_color
from kivymd.uix.menu import MDDropdownMenu

from ui.fields.dropdown import FDDropDown


class FDColor(FDDropDown):
	''' Выпадающий список выбора цвета '''

	def open_menu(self, *_) -> None:
		if self.dropdown_menu is None:
			menu_items = [
				{
					'text': element,
					'viewclass': 'OneLineListItem',
					'height': dp(50),
					'bg_color': element,
					'on_release': lambda elem=element: self.menu_callback(elem)
				} for element in self.elements
			]

			self.dropdown_menu = MDDropdownMenu(
				caller=self.ids.button,
				items=menu_items,
				width_mult=4
			)

		self.dropdown_menu.open()

	def set_value(self, element: str) -> None:
		if element in self.elements:
			self.ids.button.text = element
			self.ids.button.md_bg_color = parse_color(element)