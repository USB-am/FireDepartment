class DBAddError(Exception):
	''' Поля ввода заполнены неверно. '''


class DBCommitError(Exception):
	''' Получены неверный данные при записи. '''