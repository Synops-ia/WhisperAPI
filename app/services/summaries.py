from fastapi import File, UploadFile, Depends, Form
import torch
from redis.commands.json.path import Path
from transformers import pipeline, AutoProcessor, WhisperForConditionalGeneration
from openai import AsyncOpenAI
from ..config import settings
from ..redis_cache import redis_client
from uuid import uuid4, UUID
from .cache import get_transcript as cache_service



level = {
    "1": "You receive the transcription of an audio from a talk, conference, podcast or a text document. In both case, try to make a summarization with the most important information, be very concise, use some paragraphs but also bullet points en.",
    "2":"You receive the transcription of an audio from a talk, conference, podcast or a text document. In both case, try to make a summarization with the most important information, be a little bit concise, use some paragraphs but also bullet points.",
    "3":"You receive the transcription of an audio from a talk, conference, podcast or a text document. In both case, try to make a summarization with the most important information, be wordy, use some paragraphs but also bullet points.",
    "4":"You receive the transcription of an audio from a talk, conference, podcast or a text document. In both case, try to make a summarization with the most important information be very wordy, use some paragraphs but also bullet points, all details must be there."
}

language = {
    "en" : "anglais",
    "fr" : "francais"
}


async def add_summary(input_file : UploadFile = File(...)):
    transcript_id=uuid4()
    filename=""
    transcription=""
    if input_file.content_type == "audio/mpeg":
        speech = await input_file.read()
        transcription = __transcribe(speech)
        redis_client.json().set("transcript:{}".format(transcript_id), Path.root_path(), {
            "fileName": filename,
            "data": transcription
        })

    elif input_file.content_type == "text/plain":
        transcription = await input_file.read()
    

    else:
        raise ValueError("File must have content type audio/mpeg or text/plain")
    

    summary = await __summarize(transcription, filename=input_file.filename, transcript_id=transcript_id)
    return summary

async def retry_summary(transcript_id,complexity, locale):
    transcription = cache_service.get_summary(transcript_id)
    new_summary = await __summarize(transcription.data, transcription.fileName, transcript_id, complexity, locale)
    return new_summary



def __transcribe(speech):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    checkpoint = "openai/whisper-small"
    model = WhisperForConditionalGeneration.from_pretrained(checkpoint)
    processor = AutoProcessor.from_pretrained(checkpoint)
    whisper_pipeline = pipeline("automatic-speech-recognition",
                                model=model,
                                tokenizer=processor.tokenizer,
                                feature_extractor=processor.feature_extractor,
                                chunk_length_s=30,
                                device=device
                                )
    transcription = whisper_pipeline(speech)['text']
    return transcription


async def __summarize(transcription: str, filename: str = "", transcript_id: UUID = "", complexity: str = "1", locale: str="en"):
    client = AsyncOpenAI(
        api_key=settings.openai_api_key
    )

    chat_completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
                "content": f"{level[complexity]} en {language[locale]} "},
            {"role": "user", "content": transcription}
        ],
        max_tokens=1000
    )
    summary = chat_completion.choices[0].message.content
    redis_client.json().set("summary:{}".format(transcript_id), Path.root_path(), {
        "fileName": filename,
        "data": summary
    })
    return summary
