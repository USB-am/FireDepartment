# from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from data_base import db, Emergency


class ExpansionEmergencyElement(MDBoxLayout):
	''' Выпадающее содержимое элемента списка '''

	def __init__(self, element: Emergency):
		self.element = element

		super().__init__()


class FDExpansionPanel(MDExpansionPanel):
	''' Элемент списка с выпадающим содержимым '''

	def __init__(self, element: db.Model, content: MDBoxLayout):
		self.element = element
		self.icon = element.icon
		self.content = content(element)
		self.panel_cls = MDExpansionPanelOneLine(text=element.title)

		super().__init__()