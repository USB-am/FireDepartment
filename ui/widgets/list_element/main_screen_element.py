from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine

from data_base import Emergency
from config.paths import __WIDGET_LIST_ELEMENT_MAIN


Builder.load_file(__WIDGET_LIST_ELEMENT_MAIN)


class IconNumberLayout(MDBoxLayout):
	''' Иконка | Значение '''

	icon = StringProperty()
	value = StringProperty()


class _MainScreenElementContent(MDBoxLayout):
	''' Содержимое выдапающего списка '''

	def __init__(self, emergency: Emergency):
		self.emergency = emergency

		super().__init__()

		self.ids.icons_container.add_widget(IconNumberLayout(
			icon='pound',
			value=str(len(emergency.tags))
		))
		self.ids.icons_container.add_widget(IconNumberLayout(
			icon='account-group',
			value=str(len(emergency.humans))
		))
		if emergency.urgent:
			self.ids.icons_container.add_widget(IconNumberLayout(
				icon='truck-fast',
				value=''
			))


class MainScreenElement(MDExpansionPanel):
	''' Элемент списка на главной странице '''

	def __init__(self, emergency: Emergency):
		super().__init__(
			icon=Emergency.icon,
			content=_MainScreenElementContent(emergency),
			panel_cls=MDExpansionPanelTwoLine(
				text=emergency.title,
				secondary_text=emergency.description,
			)
		)