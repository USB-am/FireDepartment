from os import path

from kivy.lang import Builder
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from config import ADDITION_ELEMENTS_DIR, path_manager
from data_base import db, Human, Tag
from app.tools.fields.label import FDIcon


path_to_kv_file = path.join(ADDITION_ELEMENTS_DIR, 'main_page_list_element.kv')
Builder.load_file(path_to_kv_file)


class ElementContent(MDBoxLayout):
	def __init__(self, db_row: db.Model):
		self._db_row = db_row

		super().__init__()

		self.fill_content()
		self.ids.view_button.bind(on_release=self.start_call)

	def fill_content(self) -> None:
		content = self.ids.content

		if not self._db_row.urgent:
			content.add_widget(FDIcon('truck-fast', '', size_hint=(None, 1),
			                          size=(50, self.height)))

		count_included_humans = str(len(self._db_row.humans))
		content.add_widget(FDIcon(Human.icon, count_included_humans))

		count_included_tags = str(len(self._db_row.tags))
		content.add_widget(FDIcon(Tag.icon, count_included_tags))

	def start_call(self, event: MDIconButton) -> None:
		fires_screen = path_manager.PathManager().forward('fires')
		fires_screen.add_tab(self._db_row)


class MainPageListElement(MDExpansionPanel):
	icon = 'fire-alert'

	def __init__(self, db_row: db.Model):
		self._db_row = db_row
		self.title = db_row.title
		self.urgent = db_row.urgent

		self.content = ElementContent(db_row)
		self.panel_cls = MDExpansionPanelOneLine(text=self.title)

		super().__init__()