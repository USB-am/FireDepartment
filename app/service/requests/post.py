from typing import TYPE_CHECKING, Any

from exceptions.service.requests import FDStorageNotFoundError, FDBadRequest, FDBadResponse


if TYPE_CHECKING:
    from .client import APIClient
    from .storage import AppStorage
    from kivy.network.urlrequest import UrlRequestUrllib


def _update_storage(response: UrlRequestUrllib, message: dict[str, Any]) -> None:
    try:
        access_token = message['access_token']
        refresh_token = message['refresh_token']
    except KeyError as err:
        raise FDBadResponse(f'[{type(err)}] {str(err)}')


def _raise_exception(exception: type[Exception], message: dict[str, Any]) -> None:
    exception_message = message.get('detail', str(message))
    raise exception(exception_message)


def refresh_tokens(api_client: 'APIClient', storage: 'AppStorage') -> None:
    ''' Обновить токены пользователя '''
    if (tokens := storage.get_tokens()) is None:
        raise FDStorageNotFoundError('User storage file not found!')
    refresh_token = tokens.refresh_token

    api_client.post(
        endpoint='auth/refresh',
        data={'refresh_token': refresh_token},
        on_success=_update_storage,
        on_failure=lambda _, message: _raise_exception(FDBadRequest, message)
    )
