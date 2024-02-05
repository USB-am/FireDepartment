from typing import List

from kivymd.uix.boxlayout import MDBoxLayout

from data_base import Human, Rank
from ui.widgets.triple_checkbox import FDTripleCheckbox


class NotebookPhoneContent(MDBoxLayout):
	'''
	Содержимое вкладки с контактами.

	~params:
	humans: List[Human] - список людей, участвующих в выезде.
	'''

	def __init__(self, description: str, humans: List[Human], **options):
		self.description = description
		self.humans = humans
		self.checkboxes: List[FDTripleCheckbox] = []

		super().__init__(**options)

		humans_with_rank = filter(
			lambda h: bool(h.rank),
			self.humans)
		sorted_by_rank = sorted(
			humans_with_rank,
			key=lambda h: Rank.query.get(h.rank).priority,
			reverse=True)

		for human in sorted_by_rank:
			checkbox = FDTripleCheckbox(
				normal_icon='phone',
				active_icon='phone-check',
				deactive_icon='phone-cancel',
				title=human.title,
				substring=human.phone_1 if human.phone_1 is not None else ''
			)
			self.checkboxes.append(checkbox)
			self.add_widget(checkbox)
