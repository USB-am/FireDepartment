from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.button import MDRaisedButton


Builder.load_string('''
<FDRectangleFillButton>:
	size_hint: (.8, None)
	height: dp(50)
	pos_hint: {'center_x': .5}
''')


class FDRectangleFillButton(MDRaisedButton):
	text = StringProperty()
