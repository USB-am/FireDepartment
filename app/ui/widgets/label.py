from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel


Builder.load_string('''
<FDLabel>:
	size_hint_y: None
	height: dp(50)
''')


class FDLabel(MDLabel):
	text = StringProperty()
	halign = StringProperty('center')
	font_style = StringProperty('Caption')
