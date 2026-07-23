from .base import FDException


class UserDataException(FDException):
    pass


class NotFoundUserDataError(UserDataException):
    ''' Нет файла с данными о текущем пользователе '''
