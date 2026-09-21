from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, model_validator
from typing import Optional
from datetime import datetime
import re
from app.schemas.common_user import UserCredentialsBase

# ---------------- REGISTER ----------------

class UserCreate(UserCredentialsBase):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    # Email Validation
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):

        if value is None:
            return value

        if not value.endswith("@gmail.com"):
            raise ValueError("Only Gmail addresses are allowed.")

        return value
    
    # Phone Validation
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if value is None:
            return value

        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits.")

        return value

    @model_validator(mode="after")
    def validate_contact(self):

        if self.email is None and self.phone is None:
            raise ValueError("Either email or phone is required.")

        return self
# ---------------- LOGIN ----------------

class UserLogin(BaseModel):
    email_or_phone: str
    password: str
    

# ---------------- RESPONSE ----------------

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------- UPDATE PROFILE ----------------

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):

        if value is None:
            return value

        value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank.")
        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValueError("Name cannot contain numbers or special characters.")

        if re.search(r"(.)\1\1", value.lower()):
            raise ValueError("Name cannot contain three consecutive identical characters.")

        return value
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if value is None:
            return value

        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters long."
            )

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain one lowercase letter."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain one digit."
            )

        if not re.search(
            r'[!@#$%^&*(),.?":{}|<>]',
            value
        ):
            raise ValueError(
                "Password must contain one special character."
            )

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if value is None:
            return value

        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits.")

        return value