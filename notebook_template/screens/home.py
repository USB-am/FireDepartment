import time
from typing import List, Dict, Union
from datetime import datetime
from dataclasses import dataclass

from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton

from config import HOME_KV, NAVIGATION_WIDGET_KV
from widgets.notebook import FDNotebook, FDTab
from fields.call_human import FDCallHumanField


Builder.load_file(HOME_KV)
Builder.load_file(NAVIGATION_WIDGET_KV)


@dataclass
class Emergency:
	icon = 'fire-alert'
	__tablename__ = 'Emergency'
	id: int				# db.Column(db.Integer, primary_key=True)
	title: str			# db.Column(db.String(255), nullable=False)
	description: str	# db.Column(db.Text(), nullable=True)
	urgent: bool		# db.Column(db.Boolean(), nullable=True)
	tags: list			# db.relationship('Tag', secondary=post_tags, back_populates='emergencys')
	humans: list		# db.relationship('Human', secondary=post_humans, backref='emergencys')
	shorts: list		# db.relationship('Short', secondary=post_shorts, backref='emergencys')

	def __str__(self):
		return self.title


@dataclass
class Human:
	''' Люди '''

	icon = 'account-group'
	__tablename__ = 'Human'
	id: int				# = db.Column(db.Integer, primary_key=True)
	title: str			# = db.Column(db.String(255), nullable=False)
	phone_1: str		# = db.Column(db.String(255), nullable=True)
	# phone_2: str		# = db.Column(db.String(255), nullable=True)
	is_firefigher: bool	# = db.Column(db.Boolean(), nullable=False)

	def __str__(self):
		return self.title


@dataclass
class Short:
	''' Сокращение '''

	icon = 'text-short'
	__tablename__ = 'Short'
	id: int				# = db.Column(db.Integer, primary_key=True)
	title: str			# db.Column(db.String(255), nullable=False)
	explanation: str	# = db.Column(db.Text(), nullable=True)
	into_new_line: bool	# = db.Column(db.Boolean(), nullable=False)

	def __str__(self):
		return self.title


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

	def _insert_short(self, short: Short) -> None:
		''' Вставить текст сокращения в текстовое поле "Дополнительная информация" '''
		self.insert_text(text=short.explanation, new_line=short.into_new_line)

	def insert_text(self, text: str, new_line: bool=True) -> None:
		''' Вставить текст в поле "Дополнительная информация" '''

		text_field = self.ids.addition_info
		now_datetime = datetime.now()

		#TODO: change this shit
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
			text_field.insert_text(text)


class CallTabContent(MDBoxLayout):
	''' Контент вкладки '''

	def __init__(self, emergency: Emergency):
		self._emergency = emergency
		self._human_call_logs: Dict[Log] = {}
		super().__init__()

		self.calls_tab = PhoneTabContent(
			title=emergency.title,
			description=emergency.description,
			humans=emergency.humans)
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

		if state == 0:
			return
		elif state == 1:
			logger.add_log(
				title=f'Вызов {human.title}',
				description=f'[dd.mm.yyyy HH:MM] Вызов {human.title}.')
		elif state == 2:
			logger.add_log(
				title=f'Не получен ответ от {human.title}',
				description=f'[dd.mm.yyyy HH:MM] Не получен ответ от {human.title}')

		new_log = logger.get_last_log()
		key = f'{human.title}-{human.id}'
		self._human_call_logs[key] = new_log

		return new_log


TEST_EMERGENCIES = [
	Emergency(
		id=i,
		title=f'Emergency #{i+1}',
		description=f'Description for Emergency #{i+1}',
		urgent=bool(i%2),
		tags=[],
		humans=[Human(
				id=h,
				title=f'Human #{h+1}',
				phone_1=f'8 (800) 555-35-3{h}',
				is_firefigher=bool(h%2))
			for h in range(10)],
		shorts=[Short(
				id=s,
				title=f'Short #{s+1}',
				explanation=f'Short #{s+1} for Emergency #{i+1} (HH:MM)' if bool(s%2) else f'[dd.mm.yyyy HH:MM] Short #{s+1} for Emergency #{i+1}.',
				into_new_line=bool(s%2))	# TODO: Add to production version
			for s in range(10)])
	for i in range(10)
]


class HomeScreen(Screen):
	name = 'home'

	def __init__(self, **kw):
		super().__init__(**kw)

		self.notebook = FDNotebook()
		self.ids.content.add_widget(self.notebook)

		tab = FDTab('My super Emergency', CallTabContent(TEST_EMERGENCIES[0]))
		self.notebook.add_tab(tab)
