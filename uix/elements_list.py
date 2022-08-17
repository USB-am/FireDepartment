import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from data_base import db, Emergency
from config import UIX_KV_DIR


path_to_kv_file = os.path.join(UIX_KV_DIR, 'elements_list.kv')
Builder.load_file(path_to_kv_file)


class EmergencyContentElement(MDBoxLayout):
	def __init__(self, icon: str, value: int=None):
		self.icon = icon
		self.value = '' if value is None else value

		super().__init__()


class ExpansionEmergencyElement(MDBoxLayout):
	''' Выпадающее содержимое элемента списка '''

	def __init__(self, element: Emergency):
		self.element = element
		self.size_hint = (1, None)
		self.size = (self.width, 50)

		super().__init__()

		# urgent
		if self.element.urgent:
			self.ids.emergency_elements.add_widget(
				EmergencyContentElement(icon='truck-fast'))

		# humans
		self.ids.emergency_elements.add_widget(EmergencyContentElement(
			icon='account-group',
			value=len(self.element.humans)))

		# tags
		self.ids.emergency_elements.add_widget(EmergencyContentElement(
			icon='pound',
			value=len(self.element.tags)))


class FDExpansionPanel(MDExpansionPanel):
	''' Элемент списка с выпадающим содержимым '''

	def __init__(self, element: db.Model, content: MDBoxLayout):
		self.element = element
		self.icon = element.icon
		self.content = content(element)
		self.panel_cls = MDExpansionPanelOneLine(text=element.title)

		super().__init__()