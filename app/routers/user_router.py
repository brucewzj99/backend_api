from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Dict
from ..models.user import UserModel, CreateUserModel
from ..services.user_service import UserService
from ..dependencies import get_user_service

router = APIRouter()


# # Get all users
# @router.get("/", response_model=List[UserModel])
# def get_users(user_service: UserService = Depends(get_user_service)):
#     return user_service.get_all_users()


# # Get users based on user_id
# @router.get("/{user_id}", response_model=UserModel)
# def get_single_user(
#     user_id: int, user_service: UserService = Depends(get_user_service)
# ):
#     user = user_service.get_user_by_id(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# Get users based on list of ID from JSON objects
@router.post("/get_users", response_model=List[UserModel])
def get_users_from_list_of_objects(
    items: List[Dict] = Body(...), user_service: UserService = Depends(get_user_service)
):
    return user_service.get_users_from_items(items)


# Add a new user
@router.post("/", response_model=UserModel, status_code=status.HTTP_201_CREATED)
def add_user(
    user_data: CreateUserModel, user_service: UserService = Depends(get_user_service)
):
    try:
        new_user = user_service.create_user(user_data)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Delete a user
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        user_service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"detail": "User deleted successfully"}
