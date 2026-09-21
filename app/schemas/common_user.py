from pydantic import BaseModel, field_validator
import re


class UserCredentialsBase(BaseModel):
    name: str
    password: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "Name cannot be blank."
            )

        if not re.fullmatch(
            r"[A-Za-z ]+",
            value
        ):
            raise ValueError(
                "Name cannot contain numbers or special characters."
            )

        if re.search(
            r"(.)\1\1",
            value.lower()
        ):
            raise ValueError(
                "Name cannot contain three consecutive identical characters."
            )

        return value


    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

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