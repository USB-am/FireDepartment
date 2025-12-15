from typing import Generator

from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from .base import BaseScrollScreen
from data_base.model import Calls, Emergency
from app.path_manager import PathManager
from ui.layout.label_layout import FDLabelLayout
from ui.layout.history import FDHistoryElement
from ui.layout.dialogs import CallsDialogContent


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

	if calls:
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

		self.ids.content.spacing = dp(30)
		self.bind(on_pre_enter=lambda *_: self.fill_content())
		self.fill_content()

	def fill_content(self) -> None:
		''' Заполнить контент '''

		cache = {}

		for calls in get_calls_by_dates():
			label = calls[0].start.strftime('%d %B %Y')
			label_layout = FDLabelLayout(label=label)

			for ind, call in enumerate(calls):
				emergency = cache.get(call.emergency)
				if not emergency:
					emergency = Emergency.query.get(call.emergency)
					cache[call.emergency] = emergency

				start = call.start.strftime('%H:%M:%S')
				history_element = FDHistoryElement(
					title=f'{ind+1}) {start} {emergency.title}'
				)
				history_element.bind_btn(lambda *_, c=call: self.__open_dialog(c))
				label_layout.add_content(history_element)

			self.add_content(label_layout)

	def __open_dialog(self, call: Calls) -> None:
		'''
		Открыть диалоговое окно с информацией о Вызове.

		~params:
		call: Calls - запись из таблицы Calls.
		'''

		ok_btn = MDRaisedButton(text='Ок')
		dialog = MDDialog(
			title='Информация',
			type='custom',
			content_cls=CallsDialogContent(call),
			buttons=[ok_btn]
		)
		ok_btn.bind(on_release=lambda *_: dialog.dismiss())

		dialog.open()
