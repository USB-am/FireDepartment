import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemeManager

from config import LOCALIZED, FIELDS_KV_DIR


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'drop_down.kv')
Builder.load_file(path_to_kv_file)


def get_items(items: list, callback) -> list:
	output_items = []
	colors = ThemeManager().colors

	for item in items:
		output_items.append({
			'text': item,
			'bg_color': colors[item]['700'],
			'viewclass': 'OneLineListItem',
			'on_release': lambda e=item.lower(): callback(e)
		})

	return output_items


class DropDown(MDBoxLayout):
	def __init__(self, icon: str, title: str, items: list):
		self.icon = icon
		self.title = title
		self.items = get_items(items, print)
		self.display_text = LOCALIZED.translate(title)

		super().__init__()

		self.dialog = MDDropdownMenu(
			caller=self.ids.button,
			items=self.items,
			max_height=280,
			width_mult=4
		)
		self.ids.button.bind(on_release=lambda e: self.dialog.open())

	def set_value(self, value) -> None:
		print(f'DropDown.set_value({value}) [{type(value)}]')