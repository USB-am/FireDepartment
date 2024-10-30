import time
from typing import List
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

	def __init__(self, title: str, description: str, humans: list):
		self.title = title
		self.description = description
		self.humans = humans

		super().__init__()

		for human in humans:
			h = FDCallHumanField(human=human)
			self.ids.content.add_widget(h)


@dataclass
class Log:
	timestamp: float
	title: str
	description: str


class InformationLogger(list):
	''' Логгер информации '''

	def on_click_short_btn(self, title: str, description: str) -> None:
		new_log = Log(timestamp=time.time(), title=title, description=description)
		self.append(new_log)

	#TODO: Change this shit
	def __str__(self):
		sorted_logs = sorted(self, key=lambda log: -log.timestamp)
		output = ''
		for log in sorted_logs:
			output += log.title + '\n'

		return output


class _FDShortButton(MDFlatButton):
	''' Кнопка сокращения '''

	def __init__(self, short: Short):
		self.short = short

		super().__init__(text=short.title)


class InfoTabContent(MDBoxLayout):
	''' Контент вкладки с информацией '''

	def __init__(self, shorts: List[_FDShortButton]):
		self.shorts = shorts
		self._shorts_btn: List[_FDShortButton] = []
		self.__logger = InformationLogger()

		super().__init__()

		if self.shorts:
			for short in self.shorts:
				new_short = _FDShortButton(short)
				new_short.bind(on_release=lambda *_, s=short: self._insert_short(s))
				new_short.bind(on_release=lambda *_, s=short: self.__logger.on_click_short_btn(
					title=s.title, description=s.explanation
				))

				self.ids.shorts_layout.add_widget(new_short)
				self._shorts_btn.append(new_short)
		else:
			self.ids.content.remove_widget(self.ids.shorts_layout)

		# self.ids.addition_info.bind(on_touch_up=lambda inst, _: print(inst.cursor))

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
			text_field.insert_text(' ' + text + ' ')


class CallTabContent(MDBoxLayout):
	''' Контент вкладки '''

	def __init__(self, emergency: Emergency):
		self._emergency = emergency
		super().__init__()

		self.calls_tab = PhoneTabContent(
			title=emergency.title,
			description=emergency.description,
			humans=emergency.humans)
		self.info_tab = InfoTabContent(
			shorts=emergency.shorts)

		self.ids.calls.add_widget(self.calls_tab)
		self.ids.info.add_widget(self.info_tab)


TEST_EMERGENCIES = [
	Emergency(
		id=i,
		title=f'Emergency #{i+1}',
		description=f'Description for Emergency #{i+1}',
		urgent=bool(i%2),
		tags=[],
		humans=[Human(id=h, title=f'Human #{h+1}', phone_1=f'8 (800) 555-35-3{h}', is_firefigher=bool(h%2))
			for h in range(10)],
		shorts=[Short(
				id=s,
				title=f'Short #{s+1}',
				explanation=f'Short #{s+1} for Emergency #{i+1} (HH:MM:SS)' if bool(s%2) else f'[dd.mm.yyyy HH:MM] Short #{s+1} for Emergency #{i+1}.',
				into_new_line=bool(s%2))
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
