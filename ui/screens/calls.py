import time
from typing import Any, List, Dict, Union
from datetime import datetime
from dataclasses import dataclass

from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton

from . import BaseScreen
from data_base import Human, Short, Emergency, Calls, Rank
from data_base.manager import write_entry
from exceptions.data_base import DBAddError, DBCommitError
from app.path_manager import PathManager
from ui.field.call_human import FDCallHumanField
from ui.widgets.notebook import FDNotebook, FDTab
from config import NAVIGATION_WIDGET


Builder.load_file(NAVIGATION_WIDGET)


def _get_config_value(section: str, option: str, fallback: Any='') -> Any:
	'''
	Получить значение из конфига.

	~params:
	section: str - секция конфига в которой будет идти поиск значения;
	option: str - ключ по которому будет возвращено значение;
	fallback: Any - значение при ненахождении (не может быть None).
	'''

	app = MDApp.get_running_app()
	return app.config.get(section, option, fallback=fallback)


def sorted_humans_by_rank(humans: List[Human]) -> List[Human]:
	''' Отсортировать сотрудников по Званию (Rank.priority) '''

	return sorted(humans,
	              key=lambda h: Rank.query.get(h.rank).priority,
	              reverse=True)


class PhoneTabContent(MDBoxLayout):
	''' Контент вкладки о звонках '''

	def __init__(self, title: str, description: str, humans: List[Human]):
		self.title = title
		self.description = description
		self.humans = humans
		self.human_fields: List[FDCallHumanField] = []

		super().__init__()

		for human in humans:
			human_field = FDCallHumanField(human=human)
			self.ids.content.add_widget(human_field)
			self.human_fields.append(human_field)


@dataclass
class Log:
	timestamp: float
	title: str
	description: str


class InformationLogger(list):
	''' Логгер информации '''

	def add_log(self, title: str, description: str) -> None:
		new_log = Log(timestamp=time.time(), title=title, description=description)
		self.append(new_log)

	def get_last_log(self) -> Log:
		return self[-1]

	def __str__(self):
		sorted_logs = sorted(self, key=lambda log: -log.timestamp)
		return '\n'.join(map(lambda log: log.title, sorted_logs))


class _FDShortButton(MDFlatButton):
	''' Кнопка сокращения '''

	def __init__(self, short: Short):
		self.short = short

		super().__init__(text=short.title)


class InfoTabContent(MDBoxLayout):
	''' Контент вкладки с информацией '''

	def __init__(self, shorts: List[_FDShortButton]):
		self.shorts = shorts
		self._logger = InformationLogger()
		self.start_datetime = datetime.now()

		super().__init__()

		if self.shorts:
			for short in self.shorts:
				new_short = _FDShortButton(short)
				new_short.bind(on_release=lambda *_, s=short: self._insert_short(s))
				new_short.bind(on_release=lambda *_, s=short: self._logger.add_log(
					title=s.title, description=s.explanation
				))

				self.ids.shorts_layout.add_widget(new_short)
		else:
			self.ids.content.remove_widget(self.ids.shorts_layout)

		self.ids.content.add_widget(MDBoxLayout(size_hint=(1, None), height=10))

		start_text = _get_config_value(section='call', option='start_text')
		self.insert_text(f'{start_text}\n', new_line=False)

	def _insert_short(self, short: Short) -> None:
		''' Вставить текст сокращения в текстовое поле "Дополнительная информация" '''
		self.insert_text(text=short.explanation, new_line=short.into_new_line)

	def insert_text(self, text: str, new_line: bool=True) -> None:
		''' Вставить текст в поле "Дополнительная информация" '''

		text_field = self.ids.addition_info
		now_datetime = datetime.now()

		text = text. \
			replace('yyyy', str(now_datetime.year)). \
			replace('mm', str(now_datetime.month)). \
			replace('dd', str(now_datetime.day)). \
			replace('HH', str(now_datetime.hour)). \
			replace('MM', str(now_datetime.minute)). \
			replace('SS', str(now_datetime.second))

		if new_line:
			text_field.text += f'\n{text}\n'
		else:
			text_field.text += text


class CallTabContent(MDBoxLayout):
	''' Контент вкладки '''

	def __init__(self, emergency: Emergency):
		self._emergency = emergency
		self._human_call_logs: Dict[Log] = {}
		super().__init__()

		sorted_humans = sorted_humans_by_rank(emergency.humans)
		self.calls_tab = PhoneTabContent(
			title=emergency.title,
			description=emergency.description,
			humans=sorted_humans)
		self.info_tab = InfoTabContent(
			shorts=emergency.shorts)

		for human_field in self.calls_tab.human_fields:
			human_field.checkbox.bind(
				on_release=lambda *_, hf=human_field: self.update_info_textfield(hf)
			)

		self.ids.calls.add_widget(self.calls_tab)
		self.ids.info.add_widget(self.info_tab)

	def update_info_textfield(self, human_field: FDCallHumanField) -> None:
		''' Обновить текстовое поле с дополнительной информацией '''
		log = self._add_human_call_log(human_field)
		if log:
			self.info_tab.insert_text(f'{log.description}', new_line=True)

	def _add_human_call_log(self, human_field: FDCallHumanField) -> Union[Log, None]:
		''' Добавить лог при нажатии чекбокса на поле звонка человеку '''

		cbox = human_field.checkbox
		human = human_field.human
		logger = self.info_tab._logger
		state = (cbox.state_ + 1) % 3
		human_fields = {
			'human_name': human.title,
			'human_phone_1': human.phone_1,
			'human_phone_2': human.phone_2
		}

		if state == 0:
			return
		elif state == 1:
			logger.add_log(
				title=f'Вызов {human.title}',
				description=_get_config_value('call', 'human_success').format(**human_fields))
		elif state == 2:
			logger.add_log(
				title=f'Не получен ответ от {human.title}',
				description=_get_config_value('call', 'human_unsuccess').format(**human_fields))

		new_log = logger.get_last_log()
		key = f'{human.title}-{human.id}'
		self._human_call_logs[key] = new_log

		return new_log


class CallsScreen(BaseScreen):
	'''
	Страница текущих вызовов
	'''

	name = 'calls'
	toolbar_title = 'Вызовы'

	def __init__(self, path_manager: PathManager, **options):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda *_: self._path_manager.back()
		)

		self.notebook = FDNotebook()
		self.add_content(self.notebook)

	def add_notebook_tab(self, emergency: Emergency) -> None:
		''' Добавить вкладку '''

		content = CallTabContent(emergency)
		new_tab = FDTab(emergency.title, content)
		new_tab.bind_close(lambda *_, t=new_tab: self._confirm_close_tab(t))
		self.notebook.add_tab(new_tab)

		toolbar = self.ids.toolbar
		if not toolbar.right_action_items:
			toolbar.add_right_button(
				icon='content-save',
				callback=lambda *_: self._save_call(tab=self.notebook.current_tab)
			)

	def _confirm_close_tab(self, tab: FDTab) -> None:
		''' Вывести всплывающее окно с подтверждением закрытия вызова '''

		save_btn = MDRaisedButton(text='Сохранить')
		delete_btn = MDRaisedButton(text='Удалить')
		cancel_btn = MDFlatButton(text='Отмена')

		dialog = MDDialog(
			title=f'Закрыть вкладку?',
			text='После закрытия информация будет безвозвратно удалена.',
			buttons=[save_btn, delete_btn, cancel_btn]
		)

		save_btn.bind(on_release=lambda *_, t=tab: self._save_call(t))
		save_btn.bind(on_release=lambda *_: dialog.dismiss())

		delete_btn.bind(on_release=lambda *_: self._rem_toolbar_button())
		delete_btn.bind(on_release=lambda *_: dialog.dismiss())
		delete_btn.bind(on_release=lambda *_, t=tab: self.notebook.close_tab(t))

		cancel_btn.bind(on_release=lambda *_: dialog.dismiss())

		dialog.open()

	def _save_call(self, tab: FDTab) -> None:
		''' Сохранить в БД инфоромацию о вызове '''

		info_tab = tab.content.info_tab
		info_tab.insert_text(_get_config_value(section='call', option='finish_text'), new_line=True)

		saved_call = write_entry(
			model=Calls,
			params={
				'start': info_tab.start_datetime,
				'finish': datetime.now(),
				'emergency': tab.content._emergency.id,
				'info': info_tab.ids.addition_info.text,
			}
		)
		self.notebook.close_tab(tab)
		self._rem_toolbar_button()

	def _rem_toolbar_button(self) -> None:
		''' Удалить кнопку на тулбаре, если не осталось вкладок '''

		toolbar = self.ids.toolbar
		if self.notebook.tabs_count > 0:
			return

		toolbar.rem_right_button()
