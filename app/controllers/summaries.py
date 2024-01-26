from fastapi import APIRouter, HTTPException, UploadFile, File
from ..services.summaries import add_summary as add_summary_service, retry_summary as retry_summary_service

router = APIRouter()


@router.post("/summaries", tags=["summaries"], status_code=200)
async def add_summary(input_file: UploadFile = File(...), complexity: str = "1", locale: str = "en"):
    try:
        summary = await add_summary_service(input_file, complexity, locale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"summary": summary}


@router.patch("/summaries/{transcript_id}", tags=["retry"], status_code=200)
async def retry_summary(transcript_id, complexity="1", locale="en"):
    try:
        new_summary =  await retry_summary_service(transcript_id, complexity, locale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"summary": new_summary}