import datetime

from kivy.properties import StringProperty
from kivymd.uix.picker import MDDatePicker

from ui.field.button import FDButton


class FDDate(FDButton):
	'''
	Поле ввода даты.

	~params:
	title: str - заголовок.
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
			self.ids.btn.text = 'дд.мм.гггг'
		else:
			self.ids.btn.text = date.strftime('%d.%m.%Y')
