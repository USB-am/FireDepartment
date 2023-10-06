import datetime
from typing import Union

from kivy.lang.builder import Builder
from kivymd.uix.picker import MDDatePicker, MDTimePicker

# from config.paths import __FIELD_DATE

from ui.fields.button import FDIconLabelButton, FDIconLabelDoubleButton


class FDDate(FDIconLabelButton):
	''' Поле выбора даты '''

	date_dialog = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.value = None
		self.ids.button.bind(on_release=self.open_date_dialog)

	def open_date_dialog(self, *_) -> None:
		if self.date_dialog is None:
			self.date_dialog = MDDatePicker()
			self.date_dialog.bind(
				on_save=self._on_save,
				on_cancel=self._on_cancel
			)

		self.date_dialog.open()

	def _on_save(self, _, value: datetime.date, __) -> None:
		self.ids.button.text = value.strftime('%d.%m.%Y')
		self.value = value

	def _on_cancel(self, *_) -> None:
		self.ids.button.text = self.button_text
		self.value = None

	def get_value(self) -> Union[datetime.date, None]:
		return self.value

	def set_value(self, value: datetime.date) -> None:
		self._on_save(None, value, None)


class FDDateTime(FDIconLabelDoubleButton):
	''' Поле выбора даты и времени '''

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.time_value = None
		self.date_value = None
		self.date_dialog = None
		self.time_dialog = None

		self.ids.button1.bind(on_release=self.open_date_dialog)
		self.ids.button2.bind(on_release=self.open_time_dialog)

	def open_date_dialog(self, *_) -> None:
		if self.date_dialog is None:
			self.date_dialog = MDDatePicker()
			self.date_dialog.bind(
				on_save=self._on_save_date,
				on_cancel=self._on_cancel_date
			)

		self.date_dialog.open()

	def _on_save_date(self, _, value: datetime.date, __) -> None:
		self.ids.button1.text = value.strftime('%d.%m.%Y')
		self.date_value = value

	def _on_cancel_date(self, *_) -> None:
		self.ids.button1.text = self.button1_text
		self.date_value = None

	def open_time_dialog(self, *_) -> None:
		if self.time_dialog is None:
			self.time_dialog = MDTimePicker()
			self.time_dialog.bind(
				on_save=self._on_save_time,
				on_cancel=self._on_cancel_time
			)

		self.time_dialog.open()

	def _on_save_time(self, _, time: datetime.time) -> None:
		self.time_value = time
		self.ids.button2.text = time.strftime('%H:%M:%S')

	def _on_cancel_time(self, *_) -> None:
		self.time_value = None
		self.ids.button2.text = self.button2_text

	def get_value(self) -> datetime.datetime:
		if self.date_value is None or self.time_value is None:
			return None

		return self.date_value + datetime.timedelta(
			hours=self.time_value.hour,
			minutes=self.time_value.minute,
			seconds=self.time_value.second
		)

	def set_value(self, timestamp: datetime.datetime) -> None:
		date = timestamp.date()
		self._on_save_date(None, date, None)

		time = timestamp.time()
		self._on_save_time(None, time)