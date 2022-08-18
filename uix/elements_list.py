import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from data_base import db, Emergency
from config import LOCALIZED, UIX_KV_DIR


path_to_kv_file = os.path.join(UIX_KV_DIR, 'elements_list.kv')
Builder.load_file(path_to_kv_file)


class EmergencyContentElement(MDBoxLayout):
	def __init__(self, icon: str, value: int=None):
		self.icon = icon
		self.value = '' if value is None else value

		super().__init__()


class ExpansionEmergencyElement(MDBoxLayout):
	''' Выпадающее содержимое элемента списка ЧС '''

	def __init__(self, element: Emergency):
		self.element = element

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


class ExpansionOptionsElement(MDBoxLayout):
	''' Выпадающее содержимое элемента списка настроек '''

	def __init__(self, element: db.Model):
		self.element = element
		self.create_text = LOCALIZED.translate('Create')
		self.edit_text = LOCALIZED.translate('Edit')

		super().__init__()

	def binding(self, path_manager) -> None:
		lower_table_name = self.element.__tablename__.lower()
		path_to_create = f'create_{lower_table_name}'
		path_to_edit = f'edit_{lower_table_name}_list'

		self.ids.create_button.bind(
			on_release=lambda e: path_manager.forward(path_to_create))
		self.ids.edit_button.bind(
			on_release=lambda e: path_manager.forward(path_to_edit))


class FDExpansionPanel(MDExpansionPanel):
	''' Элемент списка с выпадающим содержимым '''

	def __init__(self, element: db.Model, content: MDBoxLayout):
		self.element = element
		self.icon = element.icon
		self.content = content(element)

		if isinstance(element.title, str):
			self.panel_cls = MDExpansionPanelOneLine(text=element.title)
		else:
			self.panel_cls = MDExpansionPanelOneLine(text=element.__tablename__)

		super().__init__()