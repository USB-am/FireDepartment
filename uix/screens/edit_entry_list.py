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
		self.setup_normal_toolbar()

		self.selection_list = SelectionList()
		# self.selection_list.bind(on_selected_mode=self.set_selection_mode)
		self.selection_list.bind(on_selected=self.on_selected)
		self.selection_list.bind(on_unselected=self.on_unselected)
		self.add_widgets(self.selection_list)

	def setup_normal_toolbar(self) -> None:
		self.toolbar.title = LOCALIZED.translate(f'Edit {self.name} list')
		self.toolbar.left_action_items = [
			['arrow-left', lambda e: self.path_manager.back()]
		]
		self.toolbar.right_action_items = [
			['delete', lambda e: print('Delete method')]
		]

	def setup_selection_toolbar(self) -> None:
		self.toolbar.left_action_items = [
			['close', lambda e: self.selection_list.unselected_all()]
		]
		self.toolbar.right_action_items = [
			['delete', lambda e: print('Delete method')]
		]

	def fill_content(self) -> None:
		self.selection_list.clear_widgets()
		values = self.table.query.all()
		sorted_values = sorted(values, key=lambda val: val.title)

		for db_entry in sorted_values:
			selection_list_elem = EditSelectionElement(db_entry)
			self.selection_list.add_widget(selection_list_elem)
			selection_list_elem.binding(self.redirect_and_call)

	def set_selection_mode(self) -> None:
		if self.selection_list.selected_mode:
			self.setup_selection_toolbar()
		else:
			self.setup_normal_toolbar()

	def on_selected(self, instance: SelectionList, item: EditSelectionElement) -> None:
		self.toolbar.title = str(len(instance.get_selected_list_items()))
		self.set_selection_mode()

	def on_unselected(self, instance: SelectionList, item: EditSelectionElement) -> None:
		self.toolbar.title = str(len(instance.get_selected_list_items()))
		self.set_selection_mode()

	def redirect_and_call(self, db_entry: db.Model) -> None:
		if self.selection_list.selected_mode:
			# print('selected_mode is True')
			pass
		else:
			screen_name = f'edit_{db_entry.__tablename__}'.lower()
			next_screen = self.path_manager.forward(screen_name)
			next_screen.set_element(db_entry)