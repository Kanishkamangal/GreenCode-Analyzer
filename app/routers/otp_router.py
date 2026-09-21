from fastapi import APIRouter, HTTPException
from app.schemas.otp import (
    SendOTP,
    VerifyOTP,
    ResendOTP
)
from app.services import otp_service
from app.services import user_service
from app.schemas.user import UserCreate, UserResponse
from app.services.email_service import send_otp_email
from app.core.security import create_access_token
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.dependencies import get_db

router = APIRouter(
    prefix="/otp",
    tags=["OTP"]
)

@router.post("/send-email")
async def send_email_otp(data: SendOTP, db=Depends(get_db)):

    if not data.email:
        raise HTTPException(
            status_code=400,
            detail="Email is required."
        )

    # duplicate email
    if user_service.get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )
    # duplicate phone
    if data.phone and user_service.get_user_by_phone(db, data.phone):
        raise HTTPException(
            status_code=400,
            detail="Phone number already registered."
        )
    otp = otp_service.save_registration(

        data.email,

        {
            "name": data.name,
            "email": data.email,
            "phone": data.phone,
            "password": data.password
        }

    )

    await send_otp_email(
        data.email,
        otp
    )

    return {
        "message": "OTP sent successfully."
    }


@router.post("/resend-email")
async def resend_email_otp(data: ResendOTP):

    otp = otp_service.resend_otp(data.email)

    if not otp:
        raise HTTPException(
            status_code=400,
            detail="Registration session expired. Please register again."
        )

    await send_otp_email(
        data.email,
        otp
    )

    return {
        "message": "OTP resent successfully."
    }


@router.post("/verify-email")
async def verify_email_otp(

    data: VerifyOTP,
    db: Session = Depends(get_db)

):

    if not data.email:

        raise HTTPException(
            status_code=400,
            detail="Email is required."
        )

    if not otp_service.verify_otp(
        data.email,
        data.otp
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP."
        )

    pending_user = otp_service.get_pending_user(
        data.email
    )

    if not pending_user:

        raise HTTPException(
            status_code=400,
            detail="Registration data not found."
        )

    # create user in PostgreSQL
    user = user_service.create_user(
        db,
        UserCreate(**pending_user)
    )

    # delete temporary OTP registration
    otp_service.delete_pending_user(
        data.email
    )

    # Create JWT token
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