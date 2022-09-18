from custom_screen import CustomScrolledScreen
from data_base import db
from config import LOCALIZED
from uix import ExpansionEditListElement


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
		self.toolbar.title = LOCALIZED.translate(f'Edit {self.name} list')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())

	def fill_content(self) -> None:
		self.clear()

		for db_entry in self.table.query.all():
			element = ExpansionEditListElement(db_entry)
			element.binding(self.path_manager)
			self.add_widgets(element)