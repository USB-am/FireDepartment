import os
import json
from typing import Optional
from dataclasses import dataclass, asdict

from exceptions import NotFoundUserDataError


@dataclass
class UserData:
    id: int
    email: str
    username: str


class UserDataManager:
    def __init__(self, user_data_path: Optional[str]=None):
        if user_data_path is None:
            user_data_path = os.getcwd()

        self._path_to_user_data = os.path.join(user_data_path, 'temp_user_data.json')

    def save_user_data(self, user_data: UserData) -> None:
        with open(self._path_to_user_data, mode='w') as user_data_file:
            json.dump(asdict(user_data), user_data_file, indent=2)

    def get_user_data(self) -> UserData:
        try:

            with open(self._path_to_user_data, mode='r') as user_data_file:
                user_data = json.load(user_data_file)
                return UserData(**user_data)

        except FileNotFoundError:
            raise NotFoundUserDataError('User data file not found error!')
