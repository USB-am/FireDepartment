from typing import TYPE_CHECKING, cast, Callable

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


def refresh_tokens(client: 'APIClient',
                   storage: 'AppStorage',
                   on_success: Callable[[], None] | None = None,
                   on_failure: Callable[[dict[str, str]], None] | None = None) -> None:
    token_data = cast(TokenData, storage.get_tokens())
    client.post(
        endpoint='auth/refresh',
        data={'refresh_token': token_data.refresh_token},
        on_success=lambda _, message: (_update_tokens(storage, message), on_success and on_success()), # type: ignore
        on_failure=lambda _, message: on_failure(message) if on_failure is not None else None
    )
