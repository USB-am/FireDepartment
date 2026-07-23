import os
from typing import Any

from service.token import AccessTokenManager
from service.user_data import UserDataManager, UserData
from exceptions import NotFoundUserDataError, NotFoundTokenFileError


class CurrentUser:
    def __init__(self, user_data_path: str, token_path: str):
        if not os.path.exists(user_data_path):
            raise NotFoundUserDataError(f'File "{user_data_path}" not found!')

        if not os.path.exists(token_path):
            raise NotFoundTokenFileError(f'File "{token_path}" not found!')

        self._user_data = UserDataManager(user_data_path)
        self._token = AccessTokenManager(token_path)

    def _get_from_user_data(self, arg: str) -> Any:
        user_data = self._user_data.get_user_data()
        return getattr(user_data, arg)

    @property
    def id(self) -> int:
        return self._get_from_user_data('id')

    @property
    def email(self) -> str:
        return self._get_from_user_data('email')

    @property
    def username(self) -> str:
        return self._get_from_user_data('username')

    @property
    def access_token(self) -> str:
        return self._token.get_token('access_token')

    @property
    def refresh_token(self) -> str:
        return self._token.get_token('refresh_token')

    def save_token(self, access_token: str, refresh_token: str) -> None:
        self._token.save_token(access_token, refresh_token)

    def save_user_data(self, user_data: UserData) -> None:
        self._user_data.save_user_data(user_data)
