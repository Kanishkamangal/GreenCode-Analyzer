from pydantic import BaseModel, field_validator
from typing import Optional
import re

from app.schemas.common_user import UserCredentialsBase

class SendOTP(UserCredentialsBase):
    email: Optional[str] = None
    phone: Optional[str] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if value is None:
            return value

        value = value.strip()

        if not re.fullmatch(r"\d{10}", value):
            raise ValueError(
                "Phone number must contain exactly 10 digits."
            )

        return value

class VerifyOTP(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None

    otp: str


class ResendOTP(BaseModel):
    email: str