from kivymd.uix.button import MDRaisedButton

from uix.dialog import FDDialog, ExceptionDialogContent
from config import LOCALIZED


def Dialog(error: Exception):
	ok_button = MDRaisedButton(text=LOCALIZED.translate('Ok'))
	dialog = FDDialog(
		title=LOCALIZED.translate('Error!'),
		content=ExceptionDialogContent(
			'Возникла ошибка!\n\n'
			'Возможные причины:\n'
			'1. Одно из обязательных полей не заполнено;\n'
			'2. В поле, которое должно быть уникальным, введены '
			'неуникальные данные\n'
			'3. Просто произошла какая-то хрень :D\n\n'
			f'{error}'),
		buttons=[ok_button,]
	)
	ok_button.bind(on_release=lambda e: dialog.dismiss())

	return dialog