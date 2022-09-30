import os
import datetime

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker, MDTimePicker

from config import FIELDS_KV_DIR, LOCALIZED
from uix.help_button import HelpButton


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'date_field.kv')
Builder.load_file(path_to_kv_file)


def string_to_datetime(datetime_: str) -> datetime.datetime:
	try:
		return datetime.datetime.strptime(datetime_, '%d.%m.%Y %H:%M:%S')
	except ValueError:
		return None


class DateField(MDBoxLayout):
	''' Поле выбора даты '''

	def __init__(self, icon: str, title: str):
		self.icon = icon
		self.title = title
		self._value: datetime.date = None

		self.display_text = LOCALIZED.translate(title)
		self.date_dialog = MDDatePicker()
		self.date_dialog.bind(on_save=lambda instance, date, date_range: \
			self.set_value(date))

		super().__init__()

		self.binding()

	@property
	def value(self) -> datetime.date:
		return self._value

	@value.setter
	def value(self, val: datetime.date) -> None:
		self._value = val

		if val is not None:
			self.ids.button.text = val.strftime('%d.%m.%Y')
		else:
			self.ids.button.text = 'dd.mm.yyyy'

	def binding(self) -> None:
		self.ids.button.bind(on_release=lambda e: self.date_dialog.open())

	def set_value(self, value: datetime.date) -> None:
		self.value = value

	def get_value(self) -> datetime.date:
		return self.value


class DateTimeField(MDBoxLayout):
	''' Поле выбора даты и времени '''

	def __init__(self, icon: str, title: str, help_text: str=None):
		self.icon = icon
		self.title = title
		self.help_text = help_text
		self._value = None

		self.display_text = LOCALIZED.translate(title)

		super().__init__()

		self.time_dialog = MDTimePicker()
		self.time_dialog.bind(time=lambda instance, time: self.set_time(time))
		self.date_dialog = MDDatePicker()
		self.date_dialog.bind(on_save=lambda instance, date, date_range: \
			self.set_date(date))

		if self.help_text is not None:
			self.setup()
		self.binding()

	def setup(self) -> None:
		self.ids.top_panel.add_widget(HelpButton(
			title='Date and time picker widget.',
			text=self.help_text))

	@property
	def value(self) -> datetime.datetime:
		return self._value

	@value.setter
	def value(self, value: datetime.datetime) -> None:
		self.set_date(value.date())
		self.set_time(value.time())

		self._value = value

	def binding(self) -> None:
		self.ids.date_button.bind(on_release=lambda e: self.date_dialog.open())
		self.ids.time_button.bind(on_release=lambda e: self.time_dialog.open())

	def set_date(self, date: datetime.date) -> None:
		if date is not None:
			self.ids.date_button.text = date.strftime('%d.%m.%Y')
		else:
			self.ids.date_button.text = 'dd.mm.yyyy'

	def set_time(self, time: datetime.time) -> None:
		if time is not None:
			self.ids.time_button.text = time.strftime('%H:%M:%S')
		else:
			self.ids.time_button.text = 'HH:MM:SS'

	def set_value(self, value: datetime.datetime) -> None:
		self.value = value

	def get_value(self) -> datetime.datetime:
		datetime_str = f'{self.ids.date_button.text} {self.ids.time_button.text}'

		return string_to_datetime(datetime_str)