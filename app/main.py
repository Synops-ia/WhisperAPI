from fastapi import FastAPI

from .controllers import speech_to_text, text_summarization, process

app = FastAPI()

app.include_router(speech_to_text.router)
app.include_router(text_summarization.router)
app.include_router(process.router)
