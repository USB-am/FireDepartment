from config import LOCALIZED
from app.tools import CustomScreen
from data_base import db#, Emergency
from app.tools.fields import notebook


class Fires(CustomScreen):
	name = 'fires'

	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('arrow-left', lambda e: \
			self.path_manager_.back())
		self.toolbar.add_right_button('check-outline', lambda e: print(
			'call is finished!'))

		self.main_layout.ids.content.padding = 0
		self.notebook_ = notebook.NoteBook()
		self.add_widgets(self.notebook_)

	def add_tab(self, emergency: db.Model) -> None:
		self.notebook_.add_widget(notebook.Tab(emergency=emergency))