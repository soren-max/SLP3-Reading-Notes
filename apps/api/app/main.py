import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import chapters, notes, report, roadmap

load_dotenv()
init_db()

app = FastAPI(title="SLP3 KG-LLM Reading Notes API", version="0.1.0")

origins = os.getenv("API_CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chapters.router)
app.include_router(notes.router)
app.include_router(roadmap.router)
app.include_router(report.router)


@app.get("/health")
def health():
    return {"ok": True}
