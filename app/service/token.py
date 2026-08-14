import os
import json
from typing import Optional

from config import BASE_DIR
from exceptions import NoTokenError, NotFoundTokenFileError


class AccessToken:
    def __init__(self, path_to_token: str|None=None):
        self._path_to_token = BASE_DIR if path_to_token is None else path_to_token

    def save_token(self, access_token: str, refresh_token: str) -> None:
        with open(self._path_to_token, mode='w') as tmp_token_file:
            json.dump(
                {'access_token': access_token,
                 'refresh_token': refresh_token
                },
                tmp_token_file
            )

    def get_token(self, key: str='access_token') -> str:
        try:
            with open(self._path_to_token, mode='r') as tmp_token_file:
                token_data = json.load(tmp_token_file)

                try:
                    return token_data[key]

                except KeyError:
                    raise NoTokenError(f'User.{key} not found error!')

        except FileNotFoundError:
            raise NotFoundTokenFileError('Token file not found error!')
