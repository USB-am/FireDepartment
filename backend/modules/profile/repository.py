import uuid

from modules.utils.repository import BaseRepository
from modules.users.models import UserProfile


class UserProfileRepository(BaseRepository[UserProfile, uuid.UUID]):
    model = UserProfile
