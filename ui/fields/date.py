import datetime

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker

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

	def _on_save(self, instance: MDDatePicker, value: datetime.date, date_range: list) -> None:
		btn = self.ids.btn
		btn.text = value.strftime('%d.%m.%Y')

		self.value = value

	def _on_cancel(self, instance: MDDatePicker, value: datetime.date) -> None:
		btn = self.ids.btn
		btn.text = 'dd.mm.yyyy'

		self.value = None

	def get_value(self) -> datetime.date:
		return self.value

	def set_value(self, date: datetime.date) -> None:
		self._on_save(None, date, [])