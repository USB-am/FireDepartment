import os
import datetime

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker

from config import FIELDS_KV_DIR, LOCALIZED
from uix import FDDialog


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'date_field.kv')
Builder.load_file(path_to_kv_file)


class DateField(MDBoxLayout):
	''' Поле выбора даты '''

	def __init__(self, icon: str, title: str):
		self.icon = icon
		self.title = title

		self.display_text = LOCALIZED.translate(title)
		self.dialog = MDDatePicker(on_save=self.on_save)
		print(dir(self.dialog))

		super().__init__()

		self.binding()

	def on_save(self, instance, value, date_range) -> None:
		print(instance, type(instance), '\n',
			value, type(value), '\n',
			date_range, type(date_range), sep=' '*4)

	def binding(self) -> None:
		self.ids.button.bind(on_release=lambda e: self.dialog.open())

	def set_value(self, value: datetime.datetime) -> None:
		print(f'DateField.set_value get accepted {value}')

	def get_value(self) -> datetime.datetime:
		return datetime.datetime.today()