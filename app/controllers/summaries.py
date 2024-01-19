from fastapi import APIRouter, HTTPException, File, UploadFile
from ..services.summaries import add_summary as add_summary_service

router = APIRouter()


@router.post("/summaries", tags=["summaries"])
async def add_summary(input_file: UploadFile = File(...)):
    try:
        summary = await add_summary_service(input_file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"summary": summary}
