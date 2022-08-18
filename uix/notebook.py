# from kivy.lang import Builder
from kivymd.uix.tab import MDTabs, MDTabsBase


class FDNoteBook(MDTabs):
	''' Виджет с вкладками '''

	def __init__(self):
		super().__init__()