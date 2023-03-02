from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton

from config import paths
import data_base


Builder.load_file(paths.LIST_ITEMS)


class EmergencyContentItem(MDBoxLayout):
	''' Область с иконкой и значением '''

	icon = StringProperty()
	value = StringProperty()


class EmergencyContent(MDBoxLayout):
	''' Содержимое FDEmergencyListItem '''

	def __init__(self, model: data_base.Emergency):
		super().__init__()

		self.model = model

		humans_item = EmergencyContentItem(
			icon=data_base.Human.icon,
			value=str(len(model.humans))
		)
		self.add_widget(humans_item)

		if model.urgent:
			urgent_item = EmergencyContentItem(
				icon='run-fast',
				value=''
			)
			self.add_widget(urgent_item)

		tags_item = EmergencyContentItem(
			icon=data_base.Tag.icon,
			value=str(len(model.tags))
		)
		self.add_widget(tags_item)

		self.add_widget(MDBoxLayout())

		submit = MDIconButton(
			icon='car-emergency',
			size_hint=(None, None),
			size=(self.height, self.height)
		)
		submit.bind(on_release=lambda e: print(f'Go to {model.title}'))
		self.add_widget(submit)


class FDEmergencyListItem(MDExpansionPanel):
	''' Элемент списка Вызовов '''

	def __init__(self, model: data_base.Emergency):
		self._emergency_content = EmergencyContent(model)

		super().__init__(
			icon=model.icon,
			content=self._emergency_content,
			panel_cls=MDExpansionPanelTwoLine(
				text=model.title,
				secondary_text=model.description
			)
		)