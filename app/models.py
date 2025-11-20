from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    """User model mapping to `users` table.

    Columns:
    - id: primary key
    - email: user's email (unique)
    - last_logon: datetime of last login
    - role: user's role
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    last_logon = Column(DateTime, nullable=True)
    role = Column(String(50), nullable=False, default="user")
