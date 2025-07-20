from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    faces = relationship("Face", back_populates="owner")
    gaze_events = relationship("GazeEvent", back_populates="owner")
    protection_settings = relationship("ProtectionSetting", back_populates="owner")

class Face(Base):
    __tablename__ = "faces"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    label = Column(String, nullable=True)
    image_url = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship("User", back_populates="faces")

class GazeEvent(Base):
    __tablename__ = "gaze_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_time = Column(DateTime, default=datetime.datetime.utcnow)
    x_coord = Column(Float, nullable=False)
    y_coord = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship("User", back_populates="gaze_events")

class ProtectionSetting(Base):
    __tablename__ = "protection_settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    url_pattern = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship("User", back_populates="protection_settings")
