from .base import FDException


class AccessError(FDException):
	pass


class NoAccessTokenFileError(AccessError):
	''' Нет файла с сохраненным токеном '''


class NoAccessTokenError(AccessError):
	''' Нет токена доступа '''
