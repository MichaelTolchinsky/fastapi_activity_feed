from sqlalchemy import TIMESTAMP, Column, Integer, String, DateTime
from app.db.database import Base
from datetime import datetime


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    action = Column(String, nullable=False)
    target_id = Column(Integer, nullable=False)
    timestamp = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow
    )
