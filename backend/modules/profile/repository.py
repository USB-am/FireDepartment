import uuid

from modules.utils.repository import BaseRepository
from modules.profile.models import UserProfile


class UserProfileRepository(BaseRepository[UserProfile, uuid.UUID]):
    model = UserProfile
