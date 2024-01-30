from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .controllers import cache, summaries

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://localhost:80",
    "https://www.synopsia.fr"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600
)
prefix = "/api/v1"
app.include_router(cache.router, prefix=prefix)
app.include_router(summaries.router, prefix=prefix)
