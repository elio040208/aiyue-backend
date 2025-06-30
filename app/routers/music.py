from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import os

from app.config import AUDIO_ORIG_DIR, AUDIO_VOC_DIR, AUDIO_ACC_DIR
from app.database import SessionLocal
from app.models.music import Song
from app.schemas.music import SongOut, RewriteLyricRequest
from app.service.music import get_audio_url, download_audio, get_lyric, rewrite_lyric
from app.utils.spleeter import separate_2stems

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
def get_song_audio_url(source_id: int, request: Request):
    file_path = os.path.join(AUDIO_ORIG_DIR, f"{source_id}.mp3")
    if not os.path.isfile(file_path):
        url = get_audio_url(source_id)
        if not url:
            raise HTTPException(status_code=404, detail="音频文件未找到")
        success = download_audio(url, file_path)
        if not success:
            raise HTTPException(status_code=404, detail="音频文件下载失败")
    base_url = str(request.base_url).rstrip("/")
    return {"audio_url": f"{base_url}/{AUDIO_ORIG_DIR}/{source_id}.mp3"}

@router.post("/separate_audio/{source_id}")
def separate_audio(source_id: int, request: Request):
    origin_path = os.path.join(AUDIO_ORIG_DIR, f"{source_id}.mp3")
    vocal_path = os.path.join(AUDIO_VOC_DIR, f"{source_id}.wav")
    accompaniment_path = os.path.join(AUDIO_ACC_DIR, f"{source_id}.wav")

    if not os.path.isfile(origin_path):
        raise HTTPException(status_code=404, detail="原始音频文件不存在")

    # 如果分离文件已存在，直接返回
    if os.path.isfile(vocal_path) and os.path.isfile(accompaniment_path):
        base_url = str(request.base_url).rstrip("/")
        return {
            "vocal_path": f"{base_url}/{AUDIO_VOC_DIR}/{source_id}.wav",
            "accompaniment_path": f"{base_url}/{AUDIO_ACC_DIR}/{source_id}.wav"
        }

    # 否则执行分离
    separate_2stems(origin_path, vocal_path, accompaniment_path)

    base_url = str(request.base_url).rstrip("/")
    return {
        "vocal_path": f"{base_url}/{AUDIO_VOC_DIR}/{source_id}.wav",
        "accompaniment_path": f"{base_url}/{AUDIO_ACC_DIR}/{source_id}.wav"
    }

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
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型输出格式错误：{e}")