from .services.user_service import UserService
from .utils.memory_db import in_memory_db


def get_user_service():
    return UserService(in_memory_db)
