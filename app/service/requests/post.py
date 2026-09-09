from typing import TYPE_CHECKING, Any, Callable

from service.requests.storage import TokenData
from exceptions.service.requests import FDStorageNotFoundError, FDBadResponse


if TYPE_CHECKING:
    from .client import APIClient
    from .storage import AppStorage


def _update_storage(storage: 'AppStorage', message: dict[str, Any]) -> None:
    try:
        access_token = message['access_token']
        refresh_token = message['refresh_token']
    except KeyError as err:
        raise FDBadResponse(f'[{type(err)}] {str(err)}')

    token_data = TokenData(
        access_token=access_token,
        refresh_token=refresh_token
    )
    storage.save_token(token_data)


def refresh_tokens(client: 'APIClient',
                   storage: 'AppStorage',
                   on_success: Callable[['AppStorage', dict[str, Any]], None] | None = None,
                   on_failure: Callable[[dict[str, Any]], None] | None = None
    ) -> None:

    ''' Обновить токены пользователя '''
    def success(message: dict[str, Any]) -> None:
        _update_storage(storage, message)
        on_success(storage, message) if on_success is not None else None

    def failure(message: dict[str, Any]) -> None:
        on_failure(message) if on_failure is not None else None

    if (tokens := storage.get_tokens()) is None:
        raise FDStorageNotFoundError('User storage file not found!')
    refresh_token = tokens.refresh_token

    client.post(
        endpoint='auth/refresh',
        data={'refresh_token': refresh_token},
        on_success=lambda _, message: success(message),
        on_failure=lambda _, message: failure(message)
    )
