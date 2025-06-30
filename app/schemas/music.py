from typing import List
from pydantic import BaseModel

class SongOut(BaseModel):
    id: int
    source_id: str
    title: str
    artist: str
    album: str
    cover_url: str = None
    duration: int = None

    class Config:
        from_attributes = True

class LyricLine(BaseModel):
    time: str
    text: str

class RewriteLyricRequest(BaseModel):
    lyric: List[LyricLine]
    instruction: str