from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False)

    email = Column(String(100), unique=True, nullable=True)

    password = Column(String(255), nullable=False)

    phone = Column(String(10), unique=True, nullable=True)

    role = Column(
        String(20),
        nullable=False,
        server_default="user"
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    analyses = relationship(
        "Analysis",
        back_populates="user"
    )