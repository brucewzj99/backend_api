from typing import List, Optional, Dict
from ..models.user import CreateUserModel, UserModel
from ..utils.memory_db import in_memory_db, save_data_to_json


class UserService:
    def __init__(self, db: List[UserModel]):
        self.db = db

    # def get_all_users(self) -> List[UserModel]:
    #     return self.db

    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        for user in self.db:
            if user.id == user_id:
                return user
        return None

    def get_users_from_items(self, items: List[Dict]) -> List[UserModel]:
        valid_ids: List[int] = []

        for obj in items:
            # Check if "id" is present
            if "id" not in obj:
                continue

            # Try to parse a positive integer
            try:
                possible_id = int(obj["id"])
                if possible_id > 0:
                    valid_ids.append(possible_id)
            except (ValueError, TypeError):
                pass

        found_users: List[UserModel] = []
        # Get all users with valid ids
        for user_id in valid_ids:
            user = self.get_user_by_id(user_id)
            if user:
                found_users.append(user)

        return found_users

    def create_user(self, user_data: CreateUserModel) -> UserModel:
        # Check for duplicates (name, email, or contact_number):
        for existing_user in self.db:
            if existing_user.name == user_data.name:
                raise ValueError(f"User with name '{user_data.name}' already exists.")
            if user_data.email and existing_user.email == user_data.email:
                raise ValueError(f"User with email '{user_data.email}' already exists.")
            if (
                user_data.contact_number
                and existing_user.contact_number == user_data.contact_number
            ):
                raise ValueError(
                    f"User with contact number '{user_data.contact_number}' already exists."
                )

        # Generate next ID
        if self.db:
            new_id = max(user.id for user in self.db) + 1
        else:
            new_id = 1

        try:
            # Build the new user object
            new_user = UserModel(
                id=new_id,
                name=user_data.name,
                email=user_data.email,
                contact_number=user_data.contact_number,
            )

            # Add to database
            self.db.append(new_user)
            save_data_to_json(self.db)

            return new_user
        except Exception as e:
            raise ValueError(f"Error creating user: {e}")

    # Delete a user by ID
    def delete_user(self, user_id: int) -> None:
        for index, user in enumerate(self.db):
            if user.id == user_id:
                self.db.pop(index)
                save_data_to_json(self.db)

                return
        raise ValueError("User not found")
