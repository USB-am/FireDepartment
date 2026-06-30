import os
import json
from typing import Optional

from exceptions import NoAccessTokenError, NoAccessTokenFileError


class AccessTokenManager:
    def __init__(self):
        self._path_to_token = os.path.join(os.getcwd(), 'temp_token.json')

    def save_token(self, token: str) -> None:
        with open(self._path_to_token, mode='w') as file:
            json.dump({'token': token}, file)

    def get_token(self) -> Optional[str]:
        try:
            with open(self._path_to_token, mode='r') as file:
                token = json.load(file)

                try:
                    return token['token']
                except KeyError:
                    raise NoAccessTokenError('User access-token not found error!')

        except FileNotFoundError:
            raise NoAccessTokenFileError('Access-token file not found error!')
