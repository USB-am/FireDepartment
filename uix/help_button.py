from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

from config import LOCALIZED


class HelpButton(MDIconButton):
	''' Кнопка, включающая подсказку '''

	icon = 'chat-question'

	def __init__(self, title: str, text: str, **options):
		self.title = title
		self.text = text

		self.display_title = LOCALIZED.translate(title)
		self.display_text = text

		super().__init__(**options)

		self.ok_button = MDRaisedButton(text=LOCALIZED.translate('Ok'))
		self.dialog = MDDialog(
			title=self.display_title,
			text=self.display_text,
			buttons=[self.ok_button, ])

		self.ok_button.bind(on_release=lambda e: self.dialog.dismiss())
		self.bind(on_release=lambda e: self.dialog.open())