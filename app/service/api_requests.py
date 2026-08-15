from typing import Callable

from .api_client import APIClient
from .token import AccessToken


def refresh_user_token_request(
        api_client: APIClient,
        token: AccessToken,
        on_success: Callable,
        on_failure: Callable
) -> None:
    ''' Обновить токены доступа пользователя '''
    access_token = token.get_token('access_token')
    refresh_token = token.get_token('refresh_token')
    response = api_client.post(
        endpoint='users/refresh',
        data={},
        on_success=on_success,
        on_failure=on_failure,
        extra_headers={'Cookie': f'access_token={access_token}; refresh_token={refresh_token}'}
    )

    result = response.result
    new_access_token = result['access_token']
    new_refresh_token = result['refresh_token']

    token.save_token(new_access_token, new_refresh_token)
