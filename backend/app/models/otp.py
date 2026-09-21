from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class OTP(Base):
    __tablename__ = "otp"

    otp_id = Column(Integer, primary_key=True, index=True)

    email = Column(String(100), nullable=True)

    phone = Column(String(15), nullable=True)

    otp = Column(String(6), nullable=False)

    expires_at = Column(DateTime, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )