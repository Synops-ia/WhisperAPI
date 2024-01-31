from fastapi import APIRouter, HTTPException, UploadFile, File
from ..services.summaries import add_summary as add_summary_service, retry_summary as retry_summary_service
from uuid import uuid4, UUID
from ..redis_cache import redis_client
from redis.commands.json.path import Path

router = APIRouter()


@router.post("/summaries", tags=["summaries"], status_code=200)
async def add_summary(input_file: UploadFile = File(...), complexity: str = "1", locale: str = "en"):
    transcript_id = uuid4()
    redis_client.json().set("summary:{}".format(transcript_id), Path.root_path(), {
        "fileName": input_file.filename,
        "data": "",
        "in_process": "1"
    })
    try:
        _ = await add_summary_service(input_file, complexity, locale, transcript_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return transcript_id

@router.patch("/summaries/{transcript_id}", tags=["retry"], status_code=200)
async def retry_summary(transcript_id, complexity="1", locale="en"):
    try:
        _ = await retry_summary_service(transcript_id, complexity, locale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return transcript_id
