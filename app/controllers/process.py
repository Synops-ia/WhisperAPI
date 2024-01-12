from fastapi import APIRouter, File, UploadFile
from ..services.speech_to_text import speech_to_text as speech_to_text_service
from ..services.text_summarization import generate_summary as text_summarization_service

router = APIRouter()

@router.post("/process/", tags=["speech-to-text"])
async def process_audio(speech_file: UploadFile = File(...)):
    # Transcrire l'audio en texte
    transcription_file_path = await speech_to_text_service(speech_file)

    with open(transcription_file_path, 'rb') as f:
        transcription_file = UploadFile(filename=transcription_file_path, file=f)
        summary = await text_summarization_service(transcription_file)
    return {"summary": summary}