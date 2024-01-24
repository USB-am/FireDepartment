from kivy.lang.builder import Builder
from kivymd.uix.button import MDRectangleFlatButton

from data_base import Short


Builder.load_string('''
<FDShortField>:
	text: root.short.title
	theme_text_color: 'Custom'
	line_color: app.theme_cls.text_color[:-1] + [.1]
	font_size: dp(10)
''')


class FDShortField(MDRectangleFlatButton):
	''' Элемент на листе информации экрана Calls '''

	def __init__(self, short: Short):
		self.short = short

		super().__init__()
		self.bind(on_release=lambda *_: print(self.short.explanation))
