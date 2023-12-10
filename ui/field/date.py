import datetime

from kivy.properties import StringProperty
from kivymd.uix.picker import MDDatePicker

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

		self.ids.btn1.bind(on_release=lambda *_: self.open_time_dialog())
		self.ids.btn2.bind(on_release=lambda *_: self.open_date_dialog())

	def open_time_dialog(self) -> None:
		''' Открыть диалоговое окно выбора времени '''

		print('Open time dialog')

	def open_date_dialog(self) -> None:
		''' Открыть диалоговое окно выбора даты '''

		print('Open date dialog')
