import datetime
from typing import Union

from kivy.properties import StringProperty
from kivymd.uix.picker import MDDatePicker, MDTimePicker

from ui.field.button import FDButton, FDDoubleButton


class FDDate(FDButton):
	'''
	Поле ввода даты.

	~params:
	icon: str - иконка;
	title: str - заголовок;
	btn_text: str - текст на кнопке.
	'''

	icon = StringProperty()
	title = StringProperty()
	btn_text = StringProperty()

	def __init__(self, **options):
		self._date: datetime.date = None

		super().__init__(**options)

		self.ids.btn.bind(on_release=lambda *_: self.open_dialog())

	def open_dialog(self) -> None:
		''' Открыть диалоговое окно с выбором даты '''

		dialog = MDDatePicker()
		dialog.bind(
			on_save=lambda instance, date, range:
				self._save_value_and_close_dialog(date, dialog),
			on_cancel=lambda *_:
				self._save_value_and_close_dialog(None, dialog)
		)

		dialog.open()

	def _save_value_and_close_dialog(self, date: datetime.date, dialog: MDDatePicker) -> None:
		'''
		Сохранить и закрыть диалоговое окно.

		~params:
		date: datetime.date - новое значение даты;
		dialog: MDDatePicker - диалоговое окно.
		'''

		self.set_value(date)
		dialog.dismiss()

	def set_value(self, date: datetime.date) -> None:
		'''
		Установить значение для виджета.

		~params:
		date - дата, которая будет установлена.
		'''

		self._date = date

		if self._date is None:
			self.ids.btn.text = self.btn_text
		else:
			self.ids.btn.text = date.strftime('%d.%m.%Y')

	def get_value(self) -> Union[datetime.date, None]:
		return self._date


class FDDateTime(FDDoubleButton):
	'''
	Поле ввода даты.

	~params:
	title: str - заголовок;
	btn1_text: str - текст на кнопке 1;
	btn2_text: str - текст на кнопке 2.
	'''

	title = StringProperty()
	btn1_text = StringProperty()
	btn2_text = StringProperty()

	def __init__(self, **options):
		self._time: datetime.time = None
		self._date: datetime.date = None

		super().__init__(**options)

		self.time_button = self.ids.btn1
		self.date_button = self.ids.btn2

		self.time_button.bind(on_release=lambda *_: self.open_time_dialog())
		self.date_button.bind(on_release=lambda *_: self.open_date_dialog())

	def open_time_dialog(self) -> None:
		''' Открыть диалоговое окно выбора времени '''

		dialog = MDTimePicker()
		dialog.bind(
			on_save=lambda instance, time:
				self._save_time_and_close_dialog(time, dialog),
			on_cancel=lambda *_:
				self._save_time_and_close_dialog(None, dialog)
		)

		dialog.open()

	def _save_time_and_close_dialog(self, time: datetime.time, dialog: MDTimePicker) -> None:
		self.set_time(time)
		dialog.dismiss()

	def set_time(self, time: datetime.time) -> None:
		self._time = time

		if time is not None:
			self.time_button.text = time.strftime('%H:%M:%S')
		else:
			self.time_button.text = self.btn1_text

	def open_date_dialog(self) -> None:
		''' Открыть диалоговое окно выбора даты '''

		dialog = MDDatePicker()
		dialog.bind(
			on_save=lambda instance, date, range:
				self._save_date_and_close_dialog(date, dialog),
			on_cancel=lambda *_:
				self._save_date_and_close_dialog(None, dialog)
		)

		dialog.open()

	def _save_date_and_close_dialog(self, date: datetime.date, dialog: MDDatePicker) -> None:
		self.set_date(date)
		dialog.dismiss()

	def set_date(self, date: datetime.date) -> None:
		self._date = date

		if date is not None:
			self.date_button.text = date.strftime('%d.%m.%Y')
		else:
			self.date_button.text = self.btn2_text

	def set_value(self, datetime_: Union[datetime.datetime, None]) -> None:
		if datetime_ is None:
			self.set_time(None)
			self.set_date(None)
		else:
			time = datetime_.time()
			date = datetime_.date()

			self.set_time(time)
			self.set_date(date)

	def get_value(self) -> Union[datetime.datetime, None]:
		if None in (self._date, self._time):
			return None

		return datetime.datetime.combine(self._date, self._time)
