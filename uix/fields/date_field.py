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
		self._value = None

		self.display_text = LOCALIZED.translate(title)
		self.dialog = MDDatePicker()
		self.dialog.bind(on_save=lambda instance, date, date_range: self.set_value(date))

		super().__init__()

		self.binding()

	@property
	def value(self) -> datetime.datetime:
		return self._value

	@value.setter
	def value(self, val: datetime.datetime) -> None:
		self._value = val

		if val is not None:
			self.ids.button.text = val.strftime('%d.%m.%Y')
		else:
			self.ids.button.text = 'dd.mm.yyyy'

	def binding(self) -> None:
		self.ids.button.bind(on_release=lambda e: self.dialog.open())

	def set_value(self, value: datetime.datetime) -> None:
		print(f'DateField.set_value get accepted {value}')
		self.value = value

	def get_value(self) -> datetime.datetime:
		return self.value