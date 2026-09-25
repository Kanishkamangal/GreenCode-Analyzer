from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

from app.core.config import (
    MAIL_SERVER,
    MAIL_PORT,
    MAIL_USERNAME,
    MAIL_PASSWORD,
    MAIL_FROM,
    MAIL_STARTTLS,
    MAIL_SSL_TLS,
)

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=MAIL_STARTTLS,
    MAIL_SSL_TLS=MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(
    recipient: EmailStr,
    subject: str,
    body: str,
):
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_otp_email(email: EmailStr, otp: str):

    subject = "GreenCode Analyzer - Email Verification OTP"

    body = f"""
    <h2>GreenCode Analyzer</h2>

    <p>Your OTP for email verification is:</p>

    <h1>{otp}</h1>

    <p>This OTP is valid for 5 minutes.</p>

    <p>If you did not request this, please ignore this email.</p>
    """

    await send_email(
        recipient=email,
        subject=subject,
        body=body
    )    