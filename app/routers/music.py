from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models.music import Song
from app.schemas.music import SongOut
from app.service.music import get_audio_url

router = APIRouter(prefix="/music", tags=["音乐"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/songs", response_model=List[SongOut])
def get_songs(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    songs = db.query(Song).order_by(Song.created_at.desc()).offset(offset).limit(limit).all()
    result = []
    for song in songs:
        song_data = SongOut.from_orm(song)
        song_data.audio_url = get_audio_url(song.source_id)
        result.append(song_data)
    return result