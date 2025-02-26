import json
from pathlib import Path
from typing import List
from ..models.user import UserModel

DATA_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "users.json"

in_memory_db: List[UserModel] = []


# Load data from json file into memory
def load_data_into_memory():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # clear global memory
            global in_memory_db
            in_memory_db.clear()
            # Convert dictionaries to UserModel objects
            for item in data:
                in_memory_db.append(UserModel(**item))


# Save data to json file
def save_data_to_json(db: List[UserModel]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([user.model_dump() for user in db], f, indent=4)
