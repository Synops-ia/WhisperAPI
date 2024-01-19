import redis
from fastapi import FastAPI
from .controllers import speech_to_text, cache, summaries
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
    "http://10.3.201.120:5173",
    "https://localhost.tiangolo.com",
    "http://localhost:5173",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(speech_to_text.router)
app.include_router(cache.router)

app = FastAPI()

app.include_router(summaries.router, prefix="/api/v1")