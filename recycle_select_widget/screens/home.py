from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from config import HOME_KV
from ui.fields.select import FDRecycleSelect, TempModel


Builder.load_file(HOME_KV)


class HomeScreen(Screen):
	name = 'home'

	def __init__(self, **kw):
		super().__init__(**kw)
		self.ids.content.orientation = 'vertical'

		self.ids.content.add_widget(MDBoxLayout(size_hint=(1, 1), md_bg_color=(1, 1, 1, 1)))
		select = FDRecycleSelect(
			data=[{
					'text': f'Element #{i+1}',
					'active': False,
				} for i in range(100)],
			title='Test',
			dialog_content=MDBoxLayout(),
			model=TempModel,
			group=None)
		self.ids.content.add_widget(select)
		self.ids.content.add_widget(MDBoxLayout(size_hint=(1, 1), md_bg_color=(1, 1, 1, 1)))
