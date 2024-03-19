from typing import Generator

from . import BaseScrollScreen
from data_base import Calls, Emergency
from app.path_manager import PathManager
from ui.layout.label_layout import FDLabelLayout
from ui.layout.history import FDHistoryElement


def get_calls_by_dates() -> Generator:
	''' Получить вызовы, разделенные по дате '''

	calls = Calls.query.order_by(Calls.start.desc()).all()
	output = []

	for ind in range(1, len(calls)):
		output.append(calls[ind-1])

		if calls[ind].start.date() == output[-1].start.date():
			continue

		yield output
		output = []
	yield output + [calls[-1],]


class History(BaseScrollScreen):
	''' Экран с историей завершенных вызовов '''

	name = 'history'
	toolbar_title = 'История Вызовов'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)

		self.fill_content()

	def fill_content(self) -> None:
		''' Заполнить контент '''

		cache = {}

		for calls in get_calls_by_dates():
			label = calls[0].start.strftime('%d %B %Y')
			label_layout = FDLabelLayout(label=label)

			for call in calls:
				emergency = cache.get(call.emergency)
				if not emergency:
					emergency = Emergency.query.get(call.emergency)
					cache[call.emergency] = emergency

				start = call.start.strftime('%H:%M:%S')
				label_layout.add_content(FDHistoryElement(title=f'{start} {emergency.title}'*5))

			self.add_content(label_layout)
