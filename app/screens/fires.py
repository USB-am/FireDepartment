from config import LOCALIZED
from app.tools import CustomScreen
from data_base import db, Emergency
from app.tools.fields import notebook


class Fires(CustomScreen):
	name = 'fires'

	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('arrow-left', lambda e: \
			self.path_manager_.back())
		self.toolbar.add_right_button('check-outline', lambda e: print(
			'call is finished!'))

		self.notebook_ = notebook.NoteBook()
		self.ids.widgets.add_widget(self.notebook_)

	def add_tab(self, emergency: Emergency) -> None:
		tab = notebook.TabEmergency(emergency)
		self.notebook_.add_widget(tab)

		tabs = self.notebook_.get_tab_list()
		self.notebook_.switch_tab(tabs[-1])