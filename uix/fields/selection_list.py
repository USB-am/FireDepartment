import os

from kivy.lang import Builder
from kivymd.uix.selection import MDSelectionList
from kivymd.uix.list import OneLineIconListItem

from config import FIELDS_KV_DIR
from data_base import db


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'selection_list.kv')
Builder.load_file(path_to_kv_file)


class EditSelectionElement(OneLineIconListItem):
	''' Элемент SelectionList для окна редактирования '''
	def __init__(self, entry: db.Model):
		self.entry = entry

		super().__init__()


class SelectionList(MDSelectionList):
	''' Позволяет выбирать элементы списка удерживанием тапа на элементе '''