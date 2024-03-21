from typing import Callable, List

from kivy.widgets import Widget
from kivymd.uix.boxlayout import MDBoxLayout

from data_base import Human, Emergency, Calls
from ui.widgets.notebook import NotebookPhoneContent, NotebookInfoContent
from ui.widgets.triple_checkbox import FDTripleCheckbox


class _PhoneManager:
	'''
	Менеджер экрана с номерами телефонов.

	~params:
	phone_content: NotebookPhoneContent - объект экрана с номерами телефонов.
	'''

	def __init__(self, phone_content: NotebookPhoneContent):
		self._phone_content = phone_content

	def add_phone(self, human: Human) -> None:
		'''
		Добавить номер телефона.

		~params:
		human: Human - человек, телефон которого будет добавлен.
		'''

		self._phone_content.add_widget(
			FDTripleCheckbox(normal_icon='phone',
			                 active_icon='phone-check',
			                 deactive_icon='phone-cancel',
			                 title=human.title,
			                 substring=human.phone_1 if human.phone_1 is not None else ''
			)
		)

	def bind_all(self, callback: Callable) -> None:
		''' Добавить события каждому элементу '''

		map(
			lambda c: c.ids.checkbox.bind(on_release=lambda *_: callback()),
			self._phone_content.children
		)


class _ShortsManager:
	''' Менеджер Сокращений '''

	def __init__(self, shorts_layout: MDBoxLayout):
		self._shorts_layout = shorts_layout


class _AdditionInfoManager:
	''' Менеджер дополнительной текстовой информации '''

	def __init__(self, info_field: Widget):
		self._info_field = info_field


class _CallLogManager:
	''' Менеджер логов Вызова '''

	def __init__(self, logs_layout: MDBoxLayout):
		self._logs_layout = logs_layout


class _InfoManager:
	'''
	Менеджер экрана с информацией.

	~params:
	info_content: NotebookInfoContent - объект экрана с информацией.
	'''

	def __init__(self, info_content: NotebookInfoContent):
		self._info_content = info_content

		self._shorts_layout = _ShortsManager(info_content.ids.shorts_layout)
		self._addition_info = _AdditionInfoManager(info_content.ids.addition_info_field)
		self._logs = _CallLogManager(info_content.ids.logs_layout)


class CallManager:
	'''
	Менеджер, отвечающий за хранение и обработку состояния вызова.

	~params:
	call: Emergency - вызов;
	phone_content: NotebookPhoneContent - объект вкладки с номерами телефонов;
	info_content: NotebookInfoContent - объект вкладски с дополнительной информацией.
	'''

	def __init__(self,
	             emergency: Emergency,
	             phone_content: NotebookPhoneContent,
	             info_content: NotebookInfoContent):

		self.emergency = emergency
		self.phones_manager = phone_content
		self.info_manager = info_content
