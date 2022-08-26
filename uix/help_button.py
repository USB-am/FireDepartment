from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

from config import LOCALIZED


class HelpButton(MDIconButton):
	''' Кнопка, включающая подсказку '''

	icon = 'chat-question'

	def __init__(self, title: str, text: str):
		self.title = title
		self.text = text

		self.display_title = LOCALIZED.translate(title)
		self.display_text = LOCALIZED.translate(text)

		super().__init__()

		self.dialog = MDDialog(
			title=self.display_title,
			text=self.display_text,
			buttons=[
				MDRaisedButton(text=LOCALIZED.translate('Ok')),
			])
		self.bind(on_release=lambda e: self.dialog.open())