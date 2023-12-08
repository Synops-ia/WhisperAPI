from fastapi import APIRouter, File, UploadFile
from ..services.speech_to_text import speech_to_text as speech_to_text_service
from pydantic import BaseModel
import openai

class TextRequest(BaseModel):
    text: str

openai.api_key = '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'
router = APIRouter()
client = OpenAI()

@router.post("/text-summarization/", tags=["text-summarization"])
async def generate_summary(request: TextRequest):
    try:
        # Construire le prompt
        

        # Appeler l'API GPT
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
             messages=[
                {"role": "system", "content": "You receive the transcription of an audio from a talk, conference, podcast. Try to make a summarization with the most important information, use some paragraphs but also bullet points."},
                {"role": "user", "content": f"{request.text}"}
            ],
            max_tokens=1000
)

        # Retourner la réponse de l'API GPT
        return {"response": (response.choices[0].message.content)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

