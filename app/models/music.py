from sqlalchemy import Column, Integer, String, Enum, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(64), unique=True, index=True)
    platform = Column(Enum("netease", "qq"), nullable=False)
    title = Column(String(255), nullable=False)
    artist = Column(String(255))
    album = Column(String(255))
    cover_url = Column(Text)
    audio_url = Column(Text)
    duration = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())