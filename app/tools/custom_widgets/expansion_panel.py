# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.expansionpanel import MDExpansionPanel, \
	MDExpansionPanelOneLine, MDExpansionPanelTwoLine, MDExpansionPanelThreeLine
from kivymd.uix.boxlayout import MDBoxLayout

from config import PATTERNS_DIR
from data_base import db


# path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'expansion_panel.kv')
# Builder.load_file(path_to_kv_file)


_EXPANSION_LIST_WIDGETS = {
	1: MDExpansionPanelOneLine,
	2: MDExpansionPanelTwoLine,
	3: MDExpansionPanelThreeLine,
}


def _get_expansion_list_widget():
	pass


class FDExpansionPanel(MDExpansionPanel):
	def __init__(self, db_model: db.Model, content: MDBoxLayout, text: tuple):
			self._db_model = db_model
			self._text = {key: text for key, text in \
				zip(('text', 'secondary_text', 'tertiary_text'), text)
			}

			self.icon = self._db_model.icon
			self.content = content(self._db_model)
			self.panel_cls = _EXPANSION_LIST_WIDGETS[len(text)](**self._text)
			self.size_hint = (1, None)
			self.size = (self.width, 50)

			super().__init__()