from dataclasses import dataclass
from db.db import db
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped
from datetime import datetime

@dataclass
class games(db.Model):
    __tablename__= 'games'

    id: Mapped[int] = Column(Integer, primary_key=True)
    gamenames: Mapped[str] = Column(String(256))
    description: Mapped[str] = Column(String(4096))
    playernumber: Mapped[str] = Column(String(10))
    status: Mapped[bool] = Column(Boolean(), default=True)
    is_lent: Mapped[bool] = Column(Boolean(), default=False)
    lent_at: Mapped[datetime] = Column(DateTime, nullable=True)

    user_id: Mapped[int] = Column(Integer, ForeignKey('user.id'))
    user = db.relationship("User", backref='games')