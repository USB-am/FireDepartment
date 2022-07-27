from os import path

from kivymd.uix.label import MDLabel

from data_base import Tag, Rank, Position, Human, Emergency
from app.tools.custom_screen import CustomScrolledScreen


class BaseEditList(CustomScrolledScreen):
	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('arrow-left', lambda e: \
			self.path_manager_.back())

		self.bind(on_pre_enter=lambda e: self._update_content())

	def _update_content(self) -> None:
		self.clear_scroll_content()
		elements = self.table.query.all()

		for element in elements:
			self.add_widgets(MDLabel(text=element.title, size_hint=(1, None), size=(self.width, 50)))

		print('_update_content is finished')


class TagEditList(BaseEditList):
	name = 'edit_tag_list'
	table = Tag


class RankEditList(BaseEditList):
	name = 'edit_rank_list'
	table = Rank


class PositionEditList(BaseEditList):
	name = 'edit_position_list'
	table = Position


class HumanEditList(BaseEditList):
	name = 'edit_human_list'
	table = Human


class EmergencyEditList(BaseEditList):
	name = 'edit_emergency_list'
	table = Emergency


