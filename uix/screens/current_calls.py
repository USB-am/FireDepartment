import time
from datetime import datetime

from kivymd.uix.button import MDRaisedButton

from custom_screen import CustomScreen
from config import LOCALIZED
from uix.dialog import FDDialog, ExceptionDialogContent
from uix import FDNoteBook, FDEmergencyTab, FDEmptyTab
from data_base import db, Calls
from data_base.manager import insert as DBInsert, delete as DBDelete


def Dialog() -> FDDialog:
	ok_button = MDRaisedButton(
		text=LOCALIZED.translate('Ok')
	)
	dialog = FDDialog(
		title=LOCALIZED.translate('Call error!'),
		content=ExceptionDialogContent(
			text='Возникла непредвиденная ошибка при создании нового выезда!'
		),
		buttons=[ok_button,]
	)
	ok_button.bind(on_release=lambda e: dialog.dismiss())

	return dialog


class CurrentCalls(CustomScreen):
	''' Экран текущих вызовов '''

	name = 'current_calls'

	def __init__(self, path_manager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.bind(on_enter=lambda e: self.update_tabs())

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Current calls')
		self.toolbar.add_left_button(
			'arrow-left', lambda e: self.path_manager.back())
		self.toolbar.add_right_button(
			'delete', lambda e: self.delete_record_and_close_tab())
		self.toolbar.add_right_button(
			'check-outline', lambda e: self.close_tab())

		self.notebook = FDNoteBook()
		self.add_widgets(self.notebook)

	def update_tabs(self) -> None:
		try:
			self.notebook.current_tab.tab.update()
		except AttributeError:
			pass

	def add_tab(self, element: db.Model) -> None:
		entry = self._write_db_entry(element)
		if entry is None:
			Dialog().open()
			return
		self.notebook.add_tab(FDEmergencyTab(entry))
		self.notebook.switch_to_last_tab()

	def close_tab(self) -> None:
		current_tab = self.notebook.current_tab
		self.notebook.close_tab(current_tab)
		time.sleep(.2)	# Fucking fix IndexError is pressed double-click :D

	def delete_record_and_close_tab(self) -> None:
		self.close_tab()

	def _write_db_entry(self, element: db.Model) -> Calls:
		start_time = datetime.now()
		show_start_time = start_time.strftime('%H:%M %d.%m:%Y')

		start_info = f'Вызов "{element.title}" поступил в {show_start_time}:\n\n'

		entry = DBInsert(
			model=Calls,
			values={
				'start': start_time,
				'emergency': element.id,
				'info': start_info,
			}
		)

		if entry:
			return Calls.query.all()[-1]