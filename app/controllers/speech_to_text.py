from fastapi import APIRouter, File, UploadFile
from ..services.speech_to_text import speech_to_text as speech_to_text_service

router = APIRouter()

@router.post("/speech-to-text/", tags=["speech-to-text"])
async def speech_to_text(speech_file: UploadFile = File(...)):
    text = await speech_to_text_service(speech_file)
    
    return {"transcription": text}
