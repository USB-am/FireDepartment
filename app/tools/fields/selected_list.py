from os import path

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton

from config import FIELDS_DIR, LOCALIZED, path_manager
from data_base import db
from app.tools.addition_elements.search_panel import SearchPanel


path_to_kv_file = path.join(FIELDS_DIR, 'selected_list.kv')
Builder.load_file(path_to_kv_file)


class ListElement(MDBoxLayout):
	''' Элемент списка SelectedList '''
	def __init__(self, element, group: str=None):
		self.element = element
		self.group = group
		self.display_title = element.title

		super().__init__()

	def is_active(self) -> bool:
		return self.ids.checkbox.active


class SelectedList(MDBoxLayout):
	''' Виджет выбора элементов базы данных '''
	def __init__(self, icon: str, title: str, group: str=None, show_create: bool=False):
		self.icon = icon
		self.title = title
		self.group = group
		self.elements = []

		self.display_title = LOCALIZED.translate(title)

		super().__init__()

		self.__add_top_button() if show_create else None
		self.__include_search_panel()

	def __add_top_button(self) -> None:
		top_panel = self.ids.top_panel
		add_button = MDIconButton(icon='plus', size_hint=(None, None),
		                          size=(50, 50))
		add_button_path = f'create_{self.title.lower()}'
		add_button.bind(on_release=lambda e: \
			path_manager.PathManager().forward(add_button_path))

		top_panel.add_widget(add_button)

	def __include_search_panel(self) -> None:
		search = SearchPanel()
		search.entry.callback = lambda: print('All good!')

		self.ids.search_block.add_widget(search)

	def update_content(self, values: list) -> None:
		content = self.ids.content
		content.clear_widgets()
		self.elements = []

		for element in values:
			list_element = ListElement(element, group=self.group)

			self.elements.append(list_element)
			content.add_widget(list_element)

	def filter(self) -> None:
		content = self.ids.content
		content.clear_widgets()

		# TODO: Get text from search entry
		text = 'test'
		# TODO: Find string method from get part text or use regulars
		now_elements = filter(lambda e: e.element.title == text, self.elements)

		for element in now_elements:
			list_element = ListElement(element, group=self.group)
			content.add_widget(list_element)

	def get_value(self) -> list:
		content = self.ids.content.children
		result = []

		for row in content:
			if row.is_active():
				result.append(row.element)

		return result

	def set_value(self, values: list) -> None:
		pass