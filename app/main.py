from fastapi import FastAPI

from .controllers import speech_to_text

app = FastAPI()

app.include_router(speech_to_text.router)
