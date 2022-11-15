from dataclasses import dataclass


class DataBaseException(Exception):
	''' Базовый класс ошибки в работе с базой данных '''

	msg = 'Возникла ошибка работы с базой данных!\nВозможные причины:\n'

	def __init__(self, message: str='Что-то сломалось'):
		self.message = DataBaseException.msg + message

	def __str__(self):
		return self.message


@dataclass
class TagTableError(DataBaseException):
	''' Ошибка в модели тега '''
	message: str='- Поле пустое\n'
		'- Длина названия больше 255 символов\n'
		'- Название неуникально.'


@dataclass
class RankTableError(DataBaseException):
	''' Ошибка в модели звания '''
	message: str='- Поля "Название" или "Приоритет" пустые\n'
		'- Длина названия больше 255 символов\n'
		'- Поле "Название" неуникально'


@dataclass
class PositionTableError(DataBaseException):
	''' Ошибка в модели должности '''
	message: str='- Поле "Название" пустое\n'
		'- Длина названия больше 255 символов\n'
		'- Поле "Название" неуникально'


@dataclass
class HumanTableError(DataBaseException):
	''' Ошибка в модели звания '''
	message: str='- Поле "Название" пустое\n'
		'- Длина газвания больше 255 символов\n'
		'- Поле "Название" неуникально'


@dataclass
class EmergencyTableError(DataBaseException):
	''' Ошибка в модели вызова '''
	message: str='- Поле "Название" пустое\n'
		'- Длина названия больше 255 символов\n'
		'- Поле "Название неуникально'


@dataclass
class WorktypeTableError(DataBaseException):
	''' Ошибка в модели графика работы '''
	message: str='- Какое-то из полей пустое\n'
		'- Длина названия больше 255 символов\n'
		'- Поле "Название" неуникально'