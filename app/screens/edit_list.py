from os import path

from data_base import db, Tag, Rank, Position, Human, Emergency
from app.tools.custom_screen import CustomScrolledScreen
from app.tools.addition_elements.edit_list_item import EditListItem


class BaseEditList(CustomScrolledScreen):
	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('arrow-left', lambda e: \
			self.path_manager_.back())
		self.toolbar.add_right_button('trash-can', lambda e: \
			print('delete button is pressed'))
		# delete-empty

		self.bind(on_pre_enter=lambda e: self._update_content())

	def _update_content(self) -> None:
		self.clear_scroll_content()
		elements = self.table.query.all()

		[self.add_widgets(EditListItem(element)) for element in elements]


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


