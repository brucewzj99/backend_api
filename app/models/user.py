from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, model_validator


# Model for creating a new user with validation
class CreateUserModel(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    contact_number: Optional[str] = None

    # Field-level validation for contact_number
    @field_validator("contact_number")
    def validate_contact_number(cls, value):
        if value is None:
            return value
        if len(value) != 8:
            raise ValueError("Contact number must be exactly 8 digits.")
        if value[0] not in ("9", "8", "6"):
            raise ValueError("Contact number must start with 9, 8, or 6.")
        if not value.isdigit():
            raise ValueError("Contact number must contain only digits.")
        return value

    # Model-level validation for at least one contact method
    @model_validator(mode="after")
    def at_least_one_contact_method(cls, model: "CreateUserModel") -> "CreateUserModel":
        if not model.email and not model.contact_number:
            raise ValueError("You must provide at least an email or a contact number.")
        return model


# Model for a user with an ID (for response)
class UserModel(CreateUserModel):
    id: int
