# -*- coding: utf-8 -*-

import os
import datetime

from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker

from config import PATTERNS_DIR, LOCALIZED
from app.exceptions.check_exceptions import check_none_value


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'work_day_field.kv')
Builder.load_file(path_to_kv_file)


class WorkDayField(MDBoxLayout):
	icon = 'calendar-multiselect'

	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)

		super().__init__()

		self._value = None
		self._dialog = MDDatePicker()

		self._dialog.bind(on_save=self._update_value)
		self.ids.open_calendar_button.bind(on_press=self._open_calendar)

	def _open_calendar(self, instance: MDRaisedButton) -> None:
		self._dialog.open()

	def _update_value(self, instance: MDDatePicker, date: datetime.date,\
				range_: list=[]) -> None:

		self.ids.open_calendar_button.text = date.strftime('%d.%m.%Y')
		self._value = date

	def clear(self) -> None:
		self._value = None

	def get_value(self) -> None:
		return self._value

	@check_none_value
	def set_value(self, date: datetime.date) -> None:
		self._update_value(None, date)