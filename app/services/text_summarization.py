from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from openai import OpenAI


class TextRequest(BaseModel):
    text: str

client = OpenAI()

async def generate_summary(transcription_file):
        # Construire le prompt
    contents = await transcription_file.read()
    text = contents.decode("utf-8")

        # Appeler l'API GPT
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You receive the transcription of an audio from a talk, conference, podcast. Try to make a summarization with the most important information, use some paragraphs but also bullet points."},
            {"role": "user", "content": text}
        ],
        max_tokens=1000
    )
    summary = completion.choices[0].message.content
     # Retourner la réponse de l'API GPT
    return summary

