from ui.widgets.notebook import NotebookPhoneContent, NotebookInfoContent

from data_base import Emergency, Calls


class CallManager:
	'''
	Менеджер, отвечающий за хранение и обработку состояния вызова.

	~params:
	call: Emergency - вызов;
	phone_content: NotebookPhoneContent - объект вкладки с номерами телефонов;
	info_content: NotebookInfoContent - объект вкладски с дополнительной информацией.
	'''

	def __init__(self,
		           emergency: Emergency,
		           phone_content: NotebookPhoneContent,
	             info_content: NotebookInfoContent):

		self.emergency = emergency
		self.phone_content = phone_content
		self.info_content = info_content

	@property
	def notes(self) -> str:
		''' Возвращает дополнительную информацию из текстового поля "Дополнительная информация" '''
		return self.info_content.ids.addition_info_field.text
