from typing import Union

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from config.paths import __FIELD_SELECT


Builder.load_file(__FIELD_SELECT)


class FDOption(MDBoxLayout):
	''' Элемент для поля выбора '''

	title = StringProperty()
	description = StringProperty()
	group = StringProperty(None, allownone=True)

	def hide(self) -> None:
		self.height = 0
		self.opacity = 0

	def display(self) -> None:
		self.height = dp(60)
		self.opacity = 1

	def __str__(self):
		return self.title


class FDSelect(MDBoxLayout):
	''' Поле выбора элементов '''

	icon = StringProperty()
	title = StringProperty()
	group = StringProperty(None, allownone=True)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.elements = []

		for i in range(100):
			w = FDOption(title=f'Row #{i}', description=f'Description #{i}')
			self.append(w)

	def append(self, element: Union[FDOption]) -> None:
		self.ids.container.add_widget(element)
		self.elements.append(element)

	def open_search_input(self) -> None:
		field = self.ids.search_field

		field.size_hint_x = 1
		field.hint_text = 'Найти'

	def close_search_input(self) -> None:
		field = self.ids.search_field

		field.size_hint_x = None
		field.width = 0
		field.hint_text = ''

	def change_search_state(self) -> None:
		btn = self.ids.search_button

		if btn.icon == 'magnify':
			self.open_search_input()
			btn.icon = 'close'
		else:
			self.close_search_input()
			btn.icon = 'magnify'

	def find_items(self, text: str) -> None:
		def find(element: Union[FDOption]) -> bool:
			if element.title.lower().find(text.lower()) != -1:
				return True
			if element.description.lower().find(text.lower()) != -1:
				return True
			return False

		filtered_elements = filter(find, self.elements)
		filtered_elements_list = list(filtered_elements)

		for element in self.elements:
			if element in filtered_elements_list:
				element.display()
				continue
			element.hide()
