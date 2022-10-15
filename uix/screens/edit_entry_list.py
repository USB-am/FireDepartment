from custom_screen import CustomScrolledScreen
from data_base import db
from config import LOCALIZED
# from uix import ExpansionEditListElement
from uix.fields.selection_list import SelectionList, EditSelectionElement


class EditEntryList(CustomScrolledScreen):
	''' Базовый класс со списком редактируемых элементов базы данных '''

	def __init__(self, path_manager, table: db.Model):
		super().__init__()

		self.name = f'edit_{table.__tablename__}_list'.lower()
		self.path_manager = path_manager
		self.table = table
		# self.selection_list = MDSelectionList()

		self.setup()
		self.bind(on_pre_enter=lambda e: self.fill_content())

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate(f'Edit {self.name} list')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())
		self.toolbar.add_right_button('delete', lambda e: print('Delete method'))

		self.selection_list = SelectionList()
		self.add_widgets(self.selection_list)

	def fill_content(self) -> None:
		self.selection_list.clear_widgets()
		values = self.table.query.all()
		sorted_values = sorted(values, key=lambda val: val.title)

		for db_entry in sorted_values:
			self.selection_list.add_widget(EditSelectionElement(db_entry))

		# for db_entry in sorted_values:
		# 	element = ExpansionEditListElement(db_entry)
		# 	element.binding(self.path_manager)
		# 	self.add_widgets(element)