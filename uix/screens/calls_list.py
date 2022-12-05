from typing import Union
# from datetime import strftime

from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable

from custom_screen import CustomScrolledScreen
from config import LOCALIZED
from uix import fields
from data_base import Emergency, Calls


class CallsTable(MDDataTable):
	''' Таблица для отображения списка вызовов '''
	use_pagination = True
	check = True
	column_data = [
		('№', dp(10)),
		(LOCALIZED.translate('Emergency'), dp(60)),
		(LOCALIZED.translate('Start'), dp(30)),
		(LOCALIZED.translate('Finish'), dp(30)),
	]

	def add_table(self, data: Union[list, tuple]) -> None:
		self.clear()
		valid_data = self._convert_to_valid_data(data)
		[self.add_row(_d) for _d in valid_data]

	def clear(self) -> None:
		[self.remove_row(row) for row in self.row_data]

	def _convert_to_valid_data(self, data: Union[list, type]) -> list:
		output = []

		for n, entry in enumerate(data):
			row = (
				n+1,                                    # Number
				Emergency.get(entry.emergency).title,   # Title
				entry.start.strftime('%H:%M %d.%m.%Y'), # Start datetime
				entry.finish.strftime('%H:%M %d.%m.%Y') # Finish datetime
			)
			output.append(row)

		return output


class CallsList(CustomScrolledScreen):
	''' Страница со списком всех вызовов '''

	name = 'calls_list'

	def __init__(self, path_manager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Calls list')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())

	def fill_content(self) -> None:
		self.table = CallsTable()
		self.add_widgets(self.table)

		self.fill_table()

	def fill_table(self) -> None:
		calls = Calls.query.all()
		self.table.add_table(calls)