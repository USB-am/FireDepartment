# from kivy.lang import Builder
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel

from data_base import Emergency
from uix import FDScrollFrame


class FDEmergencyTab(MDFloatLayout, MDTabsBase):
	def __init__(self, element: Emergency):
		self.element = element
		self.title = element.title

		super().__init__()

		self.scrolled_frame = FDScrollFrame()
		self.add_widget(self.scrolled_frame)

		self.setup()

	def setup(self) -> None:
		self.scrolled_frame.add_widgets(MDLabel(text=f'Tab {self.element.title}'))


class FDNoteBook(MDTabs):
	''' Виджет с вкладками '''