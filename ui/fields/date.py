import datetime
from typing import Union

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker, MDTimePicker

from config import paths


Builder.load_file(paths.DATE_FIELD)


class FDDate(MDBoxLayout):
	''' Ввод даты '''

	icon = StringProperty()
	title = StringProperty()
	value = None
	date_dialog = None

	def _open_date_dialog(self) -> None:
		if self.date_dialog is None:
			self.date_dialog = MDDatePicker()
			self.date_dialog.bind(
				on_save=self._on_save,
				on_cancel=self._on_cancel
			)

		self.date_dialog.open()

	def _on_save(self, instance: MDDatePicker, value: datetime.date, \
			date_range: list) -> None:

		btn = self.ids.btn
		btn.text = value.strftime('%d.%m.%Y')

		self.value = value

	def _on_cancel(self,
		           instance: MDDatePicker,
		           value: datetime.date
			) -> None:

		btn = self.ids.btn
		btn.text = 'dd.mm.yyyy'

		self.value = None

	def get_value(self) -> datetime.date:
		return self.value

	def set_value(self, date: datetime.date) -> None:
		self._on_save(None, date, [])


class FDDateTime(MDBoxLayout):
	''' Ввод даты и времени '''

	icon = StringProperty()
	title = StringProperty()
	date_value = None
	time_value = None
	date_dialog = None
	time_dialog = None

	def _open_date_dialog(self) -> None:
		if self.date_dialog is None:
			self.date_dialog = MDDatePicker()
			self.date_dialog.bind(
				on_save=self._on_date_save,
				on_cancel=self._on_date_cancel
			)

		self.date_dialog.open()

	def _on_date_save(self,
	                  instance: MDDatePicker,
	                  value: datetime.date,
	                  date_range: list
			) -> None:

		btn = self.ids.date_btn
		btn.text_color = [80/255, 167/255, 70/255, 1.0]
		self.date_value = value

		self._update_value_text()

	def _on_date_cancel(self,
	                    instance: MDDatePicker,
	                    value: datetime.date
			) -> None:

		btn = self.ids.date_btn
		btn.text_color = [255/255, 16/255, 16/255, 1.0]
		self.date_value = None

		self._update_value_text()

	def _open_time_dialog(self) -> None:
		if self.time_dialog is None:
			self.time_dialog = MDTimePicker()
			self.time_dialog.bind(
				on_save=self._on_time_save,
				on_cancel=self._on_time_cancel
			)

		self.time_dialog.open()

	def _on_time_save(self,
	                  instance: MDTimePicker,
	                  value: datetime.time
			) -> None:

		btn = self.ids.time_btn
		btn.text_color = [80/255, 167/255, 70/255, 1.0]
		self.time_value = value

		self._update_value_text()

	def _on_time_cancel(self,
	                    instance: MDTimePicker,
	                    value: datetime.time
			) -> None:

		btn = self.ids.time_btn
		btn.text_color = [255/255, 16/255, 16/255, 1.0]
		self.time_value = None

		self._update_value_text()

	def _update_value_text(self) -> None:
		value_text = self.ids.value_text

		if self.date_value is None:
			date_text = 'dd.mm.yyyy'
		else:
			date_text = self.date_value.strftime('%d.%m.%Y')

		if self.time_value is None:
			time_text = 'HH:MM:SS'
		else:
			time_text = self.time_value.strftime('%H:%M:%S')

		value_text.text = f'{date_text}   {time_text}'

	def get_value(self) -> datetime.datetime:
		try:
			return datetime.datetime.combine(self.date_value, self.time_value)
		except TypeError:
			return None

	def set_value(self, seted_datetime: datetime.datetime) -> None:
		date = seted_datetime.date()
		time = seted_datetime.time()

		self._on_date_save(None, date, [])
		self._on_time_save(None, time)