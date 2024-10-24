from dataclasses import dataclass

from kivy.uix.screenmanager import Screen # type: ignore
from kivy.lang.builder import Builder # type: ignore
from kivymd.uix.boxlayout import MDBoxLayout # type: ignore

from config import HOME_KV, NAVIGATION_WIDGET_KV
from widgets.notebook import FDNotebook, FDTab


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
	phone_2: str		# = db.Column(db.String(255), nullable=True)
	is_firefigher: bool	# = db.Column(db.Boolean(), nullable=False)

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
			self.ids.content.add_widget(MDLabel(text=human))


class CallTabContent(MDBoxLayout):
	''' Контент вкладки '''

	def __init__(self, emergency: Emergency):
		self._emergency = emergency
		super().__init__()

		self.calls_tab = PhoneTabContent(
			title=emergency.title,
			description=emergency.description,
			humans=emergency.humans)

		self.ids.calls.add_widget(self.calls_tab)


TEST_EMERGENCIES = [
	Emergency(id=i, title=f'Emergency #{i+1}', description=f'Description for Emergency #{i+1}',
		   urgent=bool(i%2), tags=[], humans=[], shorts=[])
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
