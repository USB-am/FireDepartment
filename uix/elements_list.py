import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from data_base import db, Emergency, ColorTheme
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


class ExpansionOptionsColorTheme(MDBoxLayout):
	''' Выпадающее содержимое элемента списка настроек (Цветовая схема) '''

	def __init__(self, element: db.Model):
		self.element = element
		self.display_text = LOCALIZED.translate('Edit')

		super().__init__()

	def binding(self, path_manager) -> None:
		lower_table_name = self.element.__tablename__.lower()
		path_to_edit = f'edit_{lower_table_name}'

		self.ids.button.bind(
			on_release=lambda e: path_manager.forward(path_to_edit))


class ExpansionEditListElement(MDBoxLayout):
	''' Элемент списка экрана редактирования '''

	def __init__(self, element: db.Model):
		self.element = element

		super().__init__()

	@property
	def text_color(self) -> tuple:
		theme = ColorTheme.query.first()
		style = theme.theme_style

		if style == 'Light':
			color = (0, 0, 0, 1)
		else:
			color = (1, 1, 1, 1)

		return color

	def binding(self, path_manager) -> None:
		def redirect_with_call(path_manager, element: db.Model) -> None:
			screen_name = f'edit_{element.__tablename__}'.lower()

			current_screen = path_manager.forward(screen_name)
			current_screen.set_element(element)

		self.ids.button.bind(on_release=lambda e: redirect_with_call(
		                                          path_manager, self.element))


class FDExpansionPanel(MDExpansionPanel):
	''' Элемент списка с выпадающим содержимым '''

	def __init__(self, element: db.Model, content: MDBoxLayout):
		self.element = element
		self.icon = element.icon
		self.content = content(element)

		try:
			if isinstance(element.title, str):
				title = element.title
			else:
				title = element.__tablename__
		except AttributeError:
			title = element.__tablename__
		self.title = LOCALIZED.translate(title)

		self.panel_cls = MDExpansionPanelOneLine(text=self.title)

		super().__init__()