from fastapi import FastAPI
import uvicorn

from app.models import User
from app.database import engine, Base
from app.routers import user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="aiyue-backend")
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
