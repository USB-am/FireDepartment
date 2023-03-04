from typing import Union

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDTextButton

from app.path_manager import PathManager
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
		submit.bind(on_release=lambda e: PathManager(None).forward('options'))
		self.add_widget(submit)


class FDEmergencyListItem(MDExpansionPanel):
	''' Элемент списка Вызовов '''

	def __init__(self, model: data_base.Emergency):
		self.model = model
		self._emergency_content = EmergencyContent(self.model)

		secondary_text = self.model.description
		if secondary_text is None:
			secondary_text = '-'

		super().__init__(
			icon=self.model.icon,
			content=self._emergency_content,
			panel_cls=MDExpansionPanelTwoLine(
				text=self.model.title,
				secondary_text=secondary_text
			)
		)


class FDHumanListItem(MDBoxLayout):
	''' Элемент списка контактов '''

	def __init__(self, model: data_base.Human):
		self.model = model

		super().__init__()

		self.ids.icon_btn.bind(on_release=self._show_info)
		self.ids.text_btn.bind(on_release=self._show_info)

	def _show_info(self, instance: Union[MDIconButton, MDTextButton]) -> None:
		print(f'You pressed on {self.model.title} button')