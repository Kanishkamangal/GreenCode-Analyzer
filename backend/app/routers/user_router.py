from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
from app.services.email_service import send_email

from app.database.dependencies import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserLogin,
    GoogleLoginRequest,
)

from app.services import user_service
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ---------------- REGISTER USER ----------------

@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    try:

        return user_service.create_user(
            db,
            user
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ---------------- LOGIN USER ----------------

@router.post("/login")
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):

    try:

        return user_service.login_user(
            db,
            login_data.email_or_phone,
            login_data.password
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ---------------- GOOGLE LOGIN ----------------

@router.post("/google")
def google_login(
    login_data: GoogleLoginRequest,
    db: Session = Depends(get_db)
):

    try:

        return user_service.google_login_user(
            db,
            login_data.credential
        )

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


# ---------------- TEST EMAIL ----------------

@router.post("/test-email")
async def test_email(
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        send_email,
        "ayushiseth1811@gmail.com",
        "GreenCode Analyzer Test",
        "<h2>Email Service Working Successfully ✅</h2>",
    )

    return {
        "message": "Email sent successfully."
    }


# ---------------- GET ALL USERS ----------------

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return user_service.get_all_users(db)


# ---------------- GET USER BY ID ----------------

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = user_service.get_user_by_id(
        db,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return user


# ---------------- UPDATE USER ----------------

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    updated_user: UserUpdate,
    db: Session = Depends(get_db),
):

    user = user_service.update_user(
        db,
        user_id,
        updated_user
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return user


# ---------------- DELETE USER ----------------

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):

    user = user_service.delete_user(
        db,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return {
        "message": "User deleted successfully."
    }