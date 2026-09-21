from sqlalchemy.orm import Session
from app.services import otp_service
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

from app.core.security import hash_password
from app.core.security import (
    verify_password,
    create_access_token
)

from app.core.config import GOOGLE_CLIENT_ID

from google.oauth2 import id_token
from google.auth.transport import requests

import secrets


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(
        User.user_id == user_id
    ).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(
        User.email == email
    ).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(
        User.phone == phone
    ).first()


# ---------------- REGISTER USER ----------------

def create_user(db: Session, user: UserCreate):

    # Check if email already exists
    if user.email:

        existing_email = get_user_by_email(
            db,
            user.email
        )

        if existing_email:
            raise ValueError(
                "Email already registered."
            )

    # Check if phone already exists
    if user.phone:

        existing_phone = get_user_by_phone(
            db,
            user.phone
        )

        if existing_phone:
            raise ValueError(
                "Phone number already registered."
            )

    # Hash password before saving
    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        phone=user.phone
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ---------------- LOGIN USER ----------------

def login_user(
    db: Session,
    email_or_phone: str,
    password: str
):

    email_or_phone = email_or_phone.strip()

    # Find user by email
    if "@" in email_or_phone:

        user = get_user_by_email(
            db,
            email_or_phone
        )

    # Otherwise search by phone
    else:

        user = get_user_by_phone(
            db,
            email_or_phone
        )

    if not user:
        raise ValueError(
            "User not found."
        )

    # Verify password
    if not verify_password(
        password,
        user.password
    ):
        raise ValueError(
            "Invalid password."
        )

    # Generate JWT Token
    access_token = create_access_token(
        data={
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "created_at": user.created_at
        }
    }


# ---------------- GOOGLE LOGIN ----------------

def google_login_user(
    db: Session,
    credential: str
):

    # --------------------------------------------------
    # Verify Google ID token
    # --------------------------------------------------

    try:

        google_user = id_token.verify_oauth2_token(
            credential,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

    except ValueError:

        raise ValueError(
            "Invalid Google authentication token."
        )

    # --------------------------------------------------
    # Extract verified information
    # --------------------------------------------------

    email = google_user.get("email")
    name = google_user.get("name")
    email_verified = google_user.get(
        "email_verified",
        False
    )

    if not email:

        raise ValueError(
            "Google account email could not be verified."
        )

    if not email_verified:

        raise ValueError(
            "Google email address is not verified."
        )

    # --------------------------------------------------
    # Check if user already exists
    # --------------------------------------------------

    user = get_user_by_email(
        db,
        email
    )

    # --------------------------------------------------
    # Create new user if not found
    # --------------------------------------------------

    if not user:

        # Fallback name in case Google doesn't provide one
        if not name:

            name = email.split("@")[0]

        # The current User model requires a password.
        # Google users don't need to know this password.
        random_password = secrets.token_urlsafe(32)

        hashed_password = hash_password(
            random_password
        )

        user = User(
            name=name,
            email=email,
            password=hashed_password,
            phone=None
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    # --------------------------------------------------
    # Generate GreenCode JWT
    # --------------------------------------------------

    access_token = create_access_token(
        data={
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role
        }
    )

    # --------------------------------------------------
    # Return same response structure as normal login
    # --------------------------------------------------

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "created_at": user.created_at
        }
    }


# ---------------- UPDATE USER ----------------

def update_user(
    db: Session,
    user_id: int,
    updated_user: UserUpdate
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        return None

    if updated_user.name is not None:

        user.name = updated_user.name

    if updated_user.phone is not None:

        user.phone = updated_user.phone

    if updated_user.password is not None:

        user.password = hash_password(
            updated_user.password
        )

    db.commit()
    db.refresh(user)

    return user


# ---------------- DELETE USER ----------------

def delete_user(
    db: Session,
    user_id: int
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        return None

    db.delete(user)
    db.commit()

    return user