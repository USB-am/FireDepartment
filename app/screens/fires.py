from config import LOCALIZED
from app.tools import CustomScreen
from data_base import db, Emergency
from app.tools.fields import notebook


class Fires(CustomScreen):
	name = 'fires'

	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('arrow-left', lambda e: \
			self.back())
		self.toolbar.add_right_button('check-outline', lambda e: \
			self.end_call())

		self.notebook_ = notebook.NoteBook()
		self.ids.widgets.add_widget(self.notebook_)

	def add_tab(self, emergency: Emergency) -> None:
		tab = notebook.TabEmergency(emergency)
		self.notebook_.add_widget(tab)

		tabs = self.notebook_.get_tab_list()
		self.notebook_.switch_tab(tabs[-1])

	def get_current_tab(self) -> notebook.TabEmergency:
		return self.notebook_.carousel.current_slide

	def end_call(self) -> None:
		# TODO: Will do the deletion of the current cell.
		pass