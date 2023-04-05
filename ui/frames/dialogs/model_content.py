from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import paths
import data_base
from ui.fields.label import FDLabelTwoLine


Builder.load_file(paths.MODEL_CONTENT_DIALOG)


class ModelDialogContenet(MDBoxLayout):
	''' Содержимое диалога с информацией о элементе базы данных '''

	def __init__(self, model: data_base.db.Model):
		self.model = model

		super().__init__()

		self.__fill()

	def __fill(self) -> None:
		columns = self.model.__table__.columns.keys()
		columns.pop(0)	# Delete 'id' column name
		content = self.ids.content

		for column in columns:
			value = getattr(self.model, column)

			if value is None:
				continue

			if not isinstance(value, str):
				value = str(value)

			label = FDLabelTwoLine(
				title=column,
				value=value
			)
			content.add_widget(label)