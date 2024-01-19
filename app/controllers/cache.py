import uuid
from fastapi import APIRouter

from ..models.cache import TranscriptModel
from ..services.cache import get_transcript as get_transcript_service
from ..services.cache import get_transcripts as get_transcripts_service
from ..services.cache import add_transcript as add_transcript_service
from ..services.cache import get_summary as get_summary_service
from ..services.cache import get_summaries as get_summaries_service

router = APIRouter()


@router.post("/transcripts")
def add_transcript(transcript: TranscriptModel):
    return add_transcript_service(uuid.uuid4().__str__(), transcript)


@router.get("/transcripts", tags=["transcripts"])
def get_transcripts():
    return get_transcripts_service()


@router.get("/transcripts/{transcript_id}", tags=["transcripts"])
def get_transcript(transcript_id: str):
    return get_transcript_service(transcript_id)


@router.get("/summaries/{transcript_id}", tags=["summaries"])
def get_summary(transcript_id: str):
    return get_summary_service(transcript_id)


@router.get("/summaries/", tags=["summaries"])
def get_summaries():
    return get_summaries_service()
