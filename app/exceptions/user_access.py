from .base import FDException


class AccessError(FDException):
	pass


class NotFoundTokenFileError(AccessError):
	''' Нет файла с сохраненным токеном '''


class NoTokenError(AccessError):
	''' Нет токена доступа '''
