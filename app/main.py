import redis
from fastapi import FastAPI
from .controllers import cache, summaries
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

app = FastAPI()
prefix = "/api/v1"
app.include_router(cache.router, prefix=prefix)
app.include_router(summaries.router, prefix=prefix)
