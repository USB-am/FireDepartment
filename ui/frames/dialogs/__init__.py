from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton


class FDDialog(MDDialog):
	''' Всплывающее окно '''

	type = 'custom'

	def __init__(self, content: MDBoxLayout):
		self.content = content

		self.ok_button = MDRaisedButton(text='OK')
		self.buttons = [self.ok_button,]

		super().__init__(content_cls=content)

		self.ok_button.bind(on_release=lambda e: self.dismiss())