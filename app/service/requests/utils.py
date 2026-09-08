from typing import TYPE_CHECKING

from service.requests.storage import TokenData


if TYPE_CHECKING:
    from .client import APIClient
    from .storage import AppStorage


def _update_tokens(storage: 'AppStorage', message: dict[str, str]) -> None:
    token_data = TokenData(
        access_token=message['access_token'],
        refresh_token=message['refresh_token']
    )
    storage.save_token(token_data)


def _raise_exception(exception: type[Exception], message: dict[str, str]) -> None:
    raise exception(message['detail'])


def refresh_tokens(client: 'APIClient', storage: 'AppStorage') -> None:
    response_data = {}
    req = client.post(
        endpoint='auth/refresh',
        data=response_data,
        on_success=lambda _, message: _update_tokens(storage, message),
        on_failure=lambda _, message: _raise_exception(AttributeError, message)
    )
