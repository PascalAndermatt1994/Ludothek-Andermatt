from dataclasses import dataclass
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped
from flask_login import UserMixin
from db.db import db
from werkzeug.security import generate_password_hash

@dataclass
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(256))
    email: Mapped[str] = Column(String(256), unique=True)
    password: Mapped[str] = Column(String(128))  # Increased length to accommodate longer hashes
    is_active: Mapped[bool] = Column(Boolean(), default=True)
    is_admin: Mapped[bool] = Column(Boolean(), default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)


