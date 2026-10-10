import os
import uvicorn
from fastapi import FastAPI
from app.config import settings
from app.database.db import engine, Base
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.user import router as user_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth")
app.include_router(user_router, prefix="/api/users")

@app.on_event("startup")
async def Start():
    Base.metadata.create_all(bind=engine)
    print("БД инициализирована")

if __name__ == "__main__":
    os.environ["NO_PROXY"] = "localhost,127.0.0.1"
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)