import uuid

from kivy.storage.jsonstore import JsonStore
from pydantic import BaseModel, EmailStr

from core.config import ApplicationConfig


class UserProfile(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str


class TokenData(BaseModel):
    access_token: str
    refresh_token: str


class AppStorage:
    def __init__(self):
        self._profile_store = JsonStore(ApplicationConfig.USER_PROFILE)
        self._service_profile = 'user_profile'
        self._service_token = 'session'

    def save_profile(self, profile: UserProfile) -> None:
        self._profile_store.put(self._service_profile, id=str(profile.id), email=profile.email, username=profile.username)

    def save_token(self, tokens: TokenData) -> None:
        self._profile_store.put(self._service_token, access_token=tokens.access_token, refresh_token=tokens.refresh_token)

    def get_profile(self) -> UserProfile | None:
        if not self._profile_store.exists(self._service_profile):
            return

        profile_store = self._profile_store.get(self._service_profile)
        return UserProfile(
            id=profile_store['id'],
            email=profile_store['email'],
            username=profile_store['username']
        )

    def get_tokens(self) -> TokenData | None:
        if not self._profile_store.exists(self._service_token):
            return

        token_store = self._profile_store.get(self._service_token)
        return TokenData(
            access_token=token_store['access_token'],
            refresh_token=token_store['refresh_token']
        )
