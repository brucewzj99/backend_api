from .services.user_service import UserService

# from .utils.memory_db import in_memory_db
from .utils.memory_db_gcs import in_memory_db
import os


def get_user_service():
    BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
    OBJECT_NAME = os.environ.get("GCS_OBJECT_NAME", "users.json")
    return UserService(in_memory_db, BUCKET_NAME, OBJECT_NAME)
