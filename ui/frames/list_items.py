from typing import Union

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, \
	MDExpansionPanelTwoLine
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDTextButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

from app.path_manager import PathManager
from config import paths
import data_base
from ui.frames.dialogs.model_content import ModelDialogContenet


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

		self._dialog = None
		self.ids.icon_btn.bind(on_release=self._show_info)
		self.ids.text_btn.bind(on_release=self._show_info)


	def _show_info(self, instance: Union[MDIconButton, MDTextButton]) -> None:
		if self._dialog is None:
			close_btn = MDRaisedButton(text='Ок')

			self._dialog = MDDialog(
				title=self.model.title,
				type='custom',
				content_cls=ModelDialogContenet(self.model),
				buttons=[
					close_btn,
				]
			)
			close_btn.bind(on_release=lambda e: self._dialog.dismiss())

		self._dialog.open()


class OptionsContent(MDBoxLayout):
	''' Содержимое элемента списка FDOptionsListItem '''

	def __init__(self, table_name: str):
		self.table_name = table_name.lower()

		super().__init__()

		self.ids.create_btn.bind(
			on_release=lambda e: PathManager(None)\
				.forward(f'create_{self.table_name}')
		)
		self.ids.edit_btn.bind(
			on_release=lambda e: PathManager(None)\
				.forward(f'edit_{self.table_name}_list')
		)


class FDOptionsListItem(MDExpansionPanel):
	''' Элемент списка в настройках '''

	def __init__(self, model: data_base.db.Model):
		self.model = model

		super().__init__(
			icon=self.model.icon,
			content=OptionsContent(self.model.__tablename__),
			panel_cls=MDExpansionPanelOneLine(text=self.model.__tablename__)
		)


class FDEditModelListItem(MDExpansionPanelOneLine):
	''' Элемент списка для редактирования '''

	def __init__(self, model: data_base.db.Model):
		self.model = model

		super().__init__()

		self.bind(on_release=self.move_to_edit_screen)

	def move_to_edit_screen(self, instance: MDExpansionPanelOneLine) -> None:
		next_screen_name = f'edit_{self.model.__tablename__.lower()}'
		next_screen = PathManager(None).forward(next_screen_name)

		next_screen.fill_content(self.model)