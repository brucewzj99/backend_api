import json
from typing import List
from google.cloud import storage
from ..models.user import UserModel

in_memory_db: List[UserModel] = []


# load data from google cloud storage
def load_data_from_gcs(bucket_name: str, object_name: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    if blob.exists():
        data_str = blob.download_as_text()
        data = json.loads(data_str)
        in_memory_db.clear()
        for item in data:
            in_memory_db.append(UserModel(**item))
    else:
        # File doesn't exist yet, so just clear db
        in_memory_db.clear()


# dump and upload to google cloud storage
def save_data_to_gcs(db: List[UserModel], bucket_name: str, object_name: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    data_list = [user.model_dump() for user in db]
    data_json = json.dumps(data_list, indent=4)

    blob.upload_from_string(data_json, content_type="application/json")
