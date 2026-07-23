import os
import json
from typing import Optional

from exceptions import NoTokenError, NotFoundTokenFileError


class AccessTokenManager:
    def __init__(self, path_to_token: str=None):
        if path_to_token is None:
            path_to_token = os.getcwd()

        self._path_to_token = os.path.join(path_to_token, 'temp_token.json')

    def save_token(self, access_token: str, refresh_token: str) -> None:
        with open(self._path_to_token, mode='w') as tmp_token_file:
            json_data = {'access_token': access_token, 'refresh_token': refresh_token}
            json.dump(json_data, tmp_token_file, indent=2)

    def get_token(self, key: str='access_token') -> str:
        try:
            with open(self._path_to_token, mode='r') as tmp_token_file:
                json_data = json.load(tmp_token_file)

                try:
                    return json_data[key]
                except KeyError:
                    raise NoTokenError('User access-token not found error!')

        except FileNotFoundError:
            raise NotFoundTokenFileError('Token file not found error!')
