from dataclasses import dataclass

from kivy.uix.screenmanager import Screen # type: ignore
from kivy.lang.builder import Builder # type: ignore
from kivymd.uix.boxlayout import MDBoxLayout # type: ignore

from config import HOME_KV
from widgets.notebook import FDNotebook, FDTab


Builder.load_file(HOME_KV)


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


class CallTabContent(MDBoxLayout):
	''' Контент вкладки '''

	def __init__(self, emergency: Emergency):
		self._emergency = emergency
		super().__init__()


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
