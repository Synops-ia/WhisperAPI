from fastapi import APIRouter, HTTPException, File, UploadFile
from ..services.summaries import SummaryRequest, add_summary as add_summary_service

router = APIRouter()


@router.post("/summaries", tags=["summaries"], status_code=200)
async def add_summary(request_file: SummaryRequest):
    try:
        summary = await add_summary_service(request_file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"summary": summary}
