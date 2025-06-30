from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models.music import Song
from app.schemas.music import SongOut, RewriteLyricRequest
from app.service.music import get_audio_url, get_lyric, rewrite_lyric

router = APIRouter(prefix="/music", tags=["音乐"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/songs", response_model=List[SongOut])
def get_songs(db: Session = Depends(get_db), limit: int = 20, offset: int = 0):
    songs = db.query(Song).order_by(Song.created_at.desc()).offset(offset).limit(limit).all()
    result = []
    for song in songs:
        song_data = SongOut.model_validate(song)
        result.append(song_data)
    return result

@router.get("/songs/{song_id}", response_model=SongOut)
def get_song_by_id(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="歌曲不存在")
    return SongOut.model_validate(song)

@router.get("/audio_url/{source_id}")
def get_song_audio_url(source_id: int):
    url = get_audio_url(source_id)
    if not url:
        raise HTTPException(status_code=404, detail="音频地址未找到")
    return {"audio_url": url}

@router.get("/lyric/{source_id}")
def get_song_lyric(source_id: int):
    lyric = get_lyric(source_id)
    if lyric is None:
        raise HTTPException(status_code=500, detail="获取歌词失败")
    return {"lyric": lyric}

@router.post("/rewrite_lyric")
def rewrite_song_lyric(request: RewriteLyricRequest):
    try:
        result = rewrite_lyric(request)
        print(f"改写后的歌词: {result}")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型输出格式错误：{e}")