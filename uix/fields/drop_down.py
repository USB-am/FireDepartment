import os

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemeManager

from config import LOCALIZED, FIELDS_KV_DIR


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'drop_down.kv')
Builder.load_file(path_to_kv_file)


COLORS = ThemeManager().colors


def gen_hue_items(items: list, callback) -> list:
	output_items = []

	for item in items:
		output_items.append({
			'text': item,
			'bg_color': COLORS['Red'][item],
			'viewclass': 'OneLineListItem',
			'on_release': lambda e=item: callback(e)
		})

	return output_items


def gen_color_items(items: list, callback) -> list:
	output_items = []

	for item in items:
		output_items.append({
			'text': item,
			'bg_color': COLORS[item]['700'],
			'viewclass': 'OneLineListItem',
			'on_release': lambda e=item: callback(e)
		})

	return output_items


class DropDown(MDBoxLayout):
	def __init__(self, icon: str, title: str):
		self.icon = icon
		self.title = title
		self.display_text = LOCALIZED.translate(title)

		super().__init__()

		self.dialog = MDDropdownMenu(
			caller=self.ids.button,
			max_height=280,
			width_mult=4
		)
		self.ids.button.bind(on_release=lambda e: self.dialog.open())

	def set_value(self, value) -> None:
		# print(f'DropDown.set_value({value}) [{type(value)}]')
		theme = MDApp.get_running_app().theme_cls

	def add(self, items: list) -> None:
		self.dialog.items.extend(items)