from typing import Union

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

from ..services.speech_to_text import speech_to_text as speech_to_text_service

router = APIRouter()


@router.post("/speech-to-text/", tags=["speech-to-text"])
async def speech_to_text(speech_file: UploadFile = File(...), uuid: Union[str, None] = None):
    transcript_id, text = await speech_to_text_service(speech_file.filename, speech_file, uuid)

    return {"transcript_id": transcript_id, "transcription": text}
