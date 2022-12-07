from typing import Union

from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable

from custom_screen import CustomScreen, CustomScrolledScreen
from config import LOCALIZED
from uix import fields
from data_base import Emergency, Calls


class CallsTable(MDDataTable):
	''' Таблица для отображения списка вызовов '''
	use_pagination = True
	check = False
	column_data = [
		('№', dp(20)),
		(LOCALIZED.translate('Emergency'), dp(60)),
		(LOCALIZED.translate('Start'), dp(30)),
		(LOCALIZED.translate('Finish'), dp(30)),
	]

	def add_table(self, data: Union[list, tuple]) -> None:
		self.clear()
		valid_data = self._convert_to_valid_data(data)
		[self.row_data.append(_d) for _d in valid_data]

	def clear(self) -> None:
		[self.remove_row(row) for row in self.row_data]

	def _convert_to_valid_data(self, data: Union[list, type]) -> list:
		output = []

		for n, entry in enumerate(data):
			start = entry.start.strftime('%H:%M %d.%m.%Y')
			if entry.finish is not None:
				finish = entry.finish.strftime('%H:%M %d.%m.%Y')
			else:
				finish = '-'
			title = Emergency.query.get(entry.emergency).title

			row = (n+1, title, start, finish)
			output.append(row)

		return output

	def _sorted_by_datetime(self, data: Union[list, tuple]) -> Union[list, tuple]:
		return zip(*sorted(enumerate(data), key=lambda d: d[1][2]))


class CallsList(CustomScreen):
	''' Страница со списком всех вызовов '''

	name = 'calls_list'

	def __init__(self, path_manager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

		self.bind(on_pre_enter=lambda e: self.fill_table())

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Calls list')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())

	def fill_content(self) -> None:
		self.table = CallsTable()
		self.add_widgets(self.table)

	def fill_table(self) -> None:
		calls = Calls.query.all()
		self.table.add_table(calls)