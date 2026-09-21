from sqlalchemy.orm import Session
from app.services import otp_service
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password
from app.core.security import (
    verify_password,
    create_access_token
)

def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

def create_user(db: Session, user: UserCreate):

    # Check if email already exists
    # If email registration
    if user.email:

        existing_email = get_user_by_email(db, user.email)

        if existing_email:
            raise ValueError("Email already registered.")

    # If phone registration
    if user.phone:

        existing_phone = get_user_by_phone(db, user.phone)

        if existing_phone:
            raise ValueError("Phone number already registered.")

    # Hash password before saving
    hashed_password = hash_password(user.password)

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

def login_user(db: Session, email_or_phone: str, password: str):

    email_or_phone = email_or_phone.strip()
    
    # Find user by email
    if "@" in email_or_phone:
        user = get_user_by_email(db, email_or_phone)

    # Otherwise search by phone
    else:
        user = get_user_by_phone(db, email_or_phone)

    if not user:
        raise ValueError("User not found.")

    # Verify password
    if not verify_password(password, user.password):
        raise ValueError("Invalid password.")

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

def update_user(db: Session, user_id: int, updated_user: UserUpdate):

    user = get_user_by_id(db, user_id)

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


def delete_user(db: Session, user_id: int):

    user = get_user_by_id(db, user_id)

    if not user:
        return None

    db.delete(user)
    db.commit()

    return user