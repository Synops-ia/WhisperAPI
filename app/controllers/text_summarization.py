from fastapi import APIRouter, File, UploadFile
from ..services.text_summarization import generate_summary as text_summarization_service
from pydantic import BaseModel
from openai import OpenAI

class TextRequest(BaseModel):
    text: str

router = APIRouter()

@router.post("/text-summarization/", tags=["text-summarization"])
async def generate_summary(transcription_file: UploadFile = File(...)):
    text = await text_summarization_service(transcription_file)

    return {"summary": text}

