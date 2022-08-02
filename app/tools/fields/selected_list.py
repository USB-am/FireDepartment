from os import path

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton

from config import FIELDS_DIR, LOCALIZED, path_manager


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

		self.display_title = LOCALIZED.translate(title)

		super().__init__()

		self.__add_top_button() if show_create else None

	def __add_top_button(self) -> None:
		top_panel = self.ids.top_panel
		add_button = MDIconButton(icon='plus', size_hint=(None, None),
		                          size=(50, 50))
		add_button_path = f'create_{self.title.lower()}'
		add_button.bind(on_release=lambda e: \
			path_manager.PathManager().forward(add_button_path))

		top_panel.add_widget(add_button)

	def update_content(self, values: list) -> None:
		content = self.ids.content
		content.clear_widgets()

		for element in values:
			content.add_widget(ListElement(element, group=self.group))

	def get_value(self) -> list:
		content = self.ids.content.children
		result = []

		for row in content:
			if row.is_active():
				result.append(row.element)

		return result