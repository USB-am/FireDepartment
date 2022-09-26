import os

from kivy.lang import Builder
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

from data_base import Emergency, Human, Rank
from uix import FDScrollFrame
from uix.dialog import FDDialog, HumanDialogContent
from config import UIX_KV_DIR


path_to_kv_file = os.path.join(UIX_KV_DIR, 'notebook.kv')
Builder.load_file(path_to_kv_file)


class HumansSelectedListElement(MDBoxLayout):
	''' Элемент списка с людьми, которым надо позвонить '''

	def __init__(self, human: Human):
		self.human = human

		super().__init__()

		dialog_button = MDRaisedButton(text='Ok')
		self.dialog = FDDialog(
			title=human.title,
			content=HumanDialogContent(human),
			buttons=[dialog_button,])

		dialog_button.bind(on_release=lambda e: self.dialog.dismiss())
		self.ids.expansion_panel.bind(on_release=lambda e: self.dialog.open())

	@property
	def phone_1(self) -> str:
		phone = self.human.phone_1
		return '-' if phone is None else phone

	@property
	def phone_2(self) -> str:
		phone = self.human.phone_2
		return '-' if phone is None else phone


class FDEmergencyTab(MDFloatLayout, MDTabsBase):
	''' Вкладка с информацией о вызовах '''

	def __init__(self, element: Emergency):
		self.element = element
		self.title = element.title

		super().__init__()

		self.setup()

	def setup(self) -> None:
		scroll_layout = self.ids.scroll_layout
		sorted_humans = sorted(
			self.element.humans,
			key=lambda human: Rank.query.get(human.rank).priority,
			reverse=True)

		[scroll_layout.add_widget(HumansSelectedListElement(human)) \
			for human in sorted_humans]


class FDNoteBook(MDTabs):
	''' Виджет с вкладками '''