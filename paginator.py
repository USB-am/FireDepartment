from time import time
from dataclasses import dataclass

from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import *
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

from data_base import Emergency


Builder.load_string('''
<MainScreen>:
	MDBoxLayout:
		orientation: 'vertical'
		size_hint: 1, 1

		Search:
			id: search
			hint_text: 'Search'

		ScrollView:
			id: scrollbar
			size_hint: 1, 1
			on_scroll_y:
				if args[1] <= 0: root.end_list_event()

			GridLayout:
				id: content
				do_scroll_x: False
				size_hint_y: None
				height: self.minimum_height
				cols: 1
				spacing: dp(10)
				padding: (dp(10), dp(20))
''')


def get_elements(widget, params):
	return tuple(
		widget(text=f'Label #{i+1}', size_hint=(1, None), height=dp(50)) \
		for i in params
	)


class Search(MDTextField):
	def __init__(self, **options):
		super().__init__(**options)
		self.callbacks = []

	def on_text_validate(self):
		output = super().on_text_validate()

		[callback(self.text) for callback in self.callbacks]

		return output


class Paginator(list):
	def __init__(self, *elements):
		super().__init__(elements)

	def paginate_by(self, count: int):
		while self:
			yield self[:count]
			self = self[count:]


@dataclass
class ElementController:
	def __init__(self, model, paginator, search):
		self.model = model
		self.paginator = paginator
		self.search = search

		# Empty generator
		self.current_paginator = iter(())

	def get_paginator(self, count=10):
		self.current_paginator = self.paginator.paginate_by(count)

		return self.current_paginator

	def find_elements(self, text):
		filtered_entries = self.model.query\
			.filter(self.model.title.like(f'%{text}%'))\
			.order_by(self.model.title)\
			.all()
		filtered_entries = [i for i in range(100)]
		self.paginator = Paginator(*get_elements(MDLabel, filtered_entries))

		return self.get_paginator()


class MainScreen(Screen):
	model = Emergency

	def __init__(self, **options):
		super().__init__(**options)

		self.paginator = Paginator(*get_elements(MDLabel, [i for i in range(100)]))
		self.last_call = 0

		self.element_controller = ElementController(
			model=self.model,
			paginator=self.paginator,
			search=self.ids.search
		)
		self.ids.search.callbacks.append(
			lambda text: self.search_elements(text)
		)

		self.elements = self.element_controller.get_paginator()
		[self.content.add_widget(el) for el in next(self.elements)]

	def search_elements(self, text):
		self.ids.content.clear_widgets()
		gen = self.element_controller.find_elements(text)
		[self.content.add_widget(el) for el in next(gen)]

	def end_list_event(self):
		if self.last_call > time() - 1:
			return

		try:
			elements = self.element_controller.current_paginator
			[self.content.add_widget(el) for el in next(elements)]
			# self.ids.scrollbar.scroll_to(self.content.children[10])
		except StopIteration:
			pass

		self.last_call = time()

	@property
	def content(self):
		return self.ids.content


class MyApp(MDApp):
	def __init__(self, *a, **kw):
		super().__init__(*a, **kw)

		self.screen = MainScreen()

	def build(self):
		return self.screen


if __name__ == '__main__':
	app = MyApp()
	app.run()
