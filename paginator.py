from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import *
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


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


class Search(MDTextField):
	def on_text_validate(self):
		output = super().on_text_validate()
		print('pressed on search')
		return output


class Paginator(list):
	def __init__(self, *elements):
		super().__init__(*elements)

	def paginate_by(self, count: int):
		while self:
			yield self[:count]
			self = self[count:]


class MainScreen(Screen):
	def __init__(self):
		super().__init__()

		self.paginator = Paginator()

		for i in range(100):
			label = MDLabel(
				text=f'Label #{i+1}',
				size_hint=(1, None),
				height=dp(50)
			)
			# self.content.add_widget(label)
			self.paginator.append(label)

		self.gen = self.paginator.paginate_by(10)
		[self.content.add_widget(el) for el in next(self.gen)]

	def end_list_event(self):
		try:
			[self.content.add_widget(el) for el in next(self.gen)]
			# elements_count = len(self.content.children)
			# to_scroll_percent = 10 / elements_count / 10
			# self.ids.scrollbar.scroll_y = to_scroll_percent
		except StopIteration:
			pass

	@property
	def content(self):
		return self.ids.content


class MyApp(MDApp):
	def __init__(self, *a, **kw):
		super().__init__(*a, **kw)

		self.screen = MainScreen()
		# self.screen.add_widget(TestBtn())

	def build(self):
		return self.screen


if __name__ == '__main__':
	app = MyApp()
	app.run()
