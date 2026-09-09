from exceptions.service.base import FDServiceException


class FDStorageException(FDServiceException):
    ''' Базовая ошибка Storage '''


class FDStorageNotFoundError(FDStorageException):
    ''' storage файл не найден '''


class FDBadRequest(FDServiceException):
    ''' Ошибка при отправке запроса '''


class FDBadResponse(FDServiceException):
    ''' Некорректный ответ сервера '''
