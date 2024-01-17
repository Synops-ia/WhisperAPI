from fastapi import FastAPI

from .controllers import summaries

app = FastAPI()

app.include_router(summaries.router, prefix="/api/v1")

