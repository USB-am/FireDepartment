from typing import Union

from kivy.properties import ListProperty, Property
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu

from ui.fields.button import FDIconLabelButton


class FDDropDown(FDIconLabelButton):
	''' Выпадающий список '''

	elements = ListProperty()
	callback = Property(None, allownone=True)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.dropdown_menu = None
		self.ids.button.bind(on_release=self.open_menu)

	def open_menu(self, *_) -> None:
		if self.dropdown_menu is None:
			menu_items = [
				{
					'text': element,
					'viewclass': 'OneLineListItem',
					'height': dp(50),
					'on_release': lambda elem=element: self.menu_callback(elem)
				} for element in self.elements
			]

			self.dropdown_menu = MDDropdownMenu(
				caller=self.ids.button,
				items=menu_items,
				width_mult=4
			)

		self.dropdown_menu.open()

	def close_menu(self, *_) -> None:
		if self.dropdown_menu is None:
			return

		self.dropdown_menu.dismiss()

	def menu_callback(self, element: str) -> None:
		self.set_value(element)
		self.close_menu()

		if self.callback is None:
			return

		return self.callback(element)

	def get_value(self) -> Union[str, None]:
		if self.ids.button.text != self.button_text:
			return self.ids.button.text

		return

	def set_value(self, element: str) -> None:
		if element in self.elements:
			self.ids.button.text = element