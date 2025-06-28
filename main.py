from fastapi import FastAPI
import uvicorn

from app.models.music import Song
from app.database import engine, Base
from app.routers import music
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="aiyue-backend")
app.include_router(music.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 你的前端地址和端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
