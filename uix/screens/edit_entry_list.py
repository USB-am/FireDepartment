from custom_screen import CustomScrolledScreen
from data_base import db
from data_base import manager as DBManager
from config import LOCALIZED
from uix.fields.selection_list import SelectionList, EditSelectionElement


class EditEntryList(CustomScrolledScreen):
	''' Базовый класс со списком редактируемых элементов базы данных '''

	def __init__(self, path_manager, table: db.Model):
		super().__init__()

		self.name = f'edit_{table.__tablename__}_list'.lower()
		self.path_manager = path_manager
		self.table = table

		self.setup()
		self.bind(on_pre_enter=lambda e: self.fill_content())

	def setup(self) -> None:
		self.selection_list = SelectionList()
		self.selection_list.bind(on_selected=lambda *e: self.on_select())
		self.selection_list.bind(on_unselected=lambda *e: self.on_unselect())
		self.add_widgets(self.selection_list)

		self.setup_normal_toolbar()

	def setup_normal_toolbar(self) -> None:
		self.toolbar.title = LOCALIZED.translate(f'Edit {self.name} list')
		self.toolbar.left_action_items = [
			['arrow-left', lambda e: self.path_manager.back()]
		]
		self.toolbar.right_action_items = [
			['delete', lambda e: self.on_select()]
		]
		self.selection_list.selected_mode = False

	def setup_selection_toolbar(self) -> None:
		self.toolbar.title = str(len(self.selection_list.\
			get_selected_list_items()))
		self.toolbar.left_action_items = [
			['close', lambda e: self.on_unselected_all()]
		]
		self.toolbar.right_action_items = [
			['delete', lambda e: self.delete_selected_items()]
		]

	def on_select(self) -> None:
		self.selection_list.selected_mode = True
		self.setup_selection_toolbar()

	def on_unselect(self) -> None:
		if len(self.selection_list.get_selected_list_items()):
			self.setup_selection_toolbar()
		else:
			self.setup_normal_toolbar()

	def on_unselected_all(self) -> None:
		self.selection_list.unselected_all()
		self.setup_normal_toolbar()

	def delete_selected_items(self) -> None:
		items = self.selection_list.get_selected_list_items()

		for item in items:
			DBManager.delete(item.instance_item.entry)

		self.fill_content()
		self.setup_normal_toolbar()

	def fill_content(self) -> None:
		self.selection_list.clear_widgets()
		values = self.table.query.all()
		sorted_values = sorted(values, key=lambda val: val.title)

		for db_entry in sorted_values:
			selection_list_elem = EditSelectionElement(db_entry)
			self.selection_list.add_widget(selection_list_elem)
			selection_list_elem.binding(self.redirect_and_call)

	def redirect_and_call(self, db_entry: db.Model) -> None:
		if not self.selection_list.selected_mode:
			screen_name = f'edit_{db_entry.__tablename__}'.lower()
			next_screen = self.path_manager.forward(screen_name)
			next_screen.set_element(db_entry)