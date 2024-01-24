from fastapi import File, UploadFile, Depends
import torch
from redis.commands.json.path import Path
from transformers import pipeline, AutoProcessor, WhisperForConditionalGeneration
from openai import AsyncOpenAI
from ..config import settings
from ..redis_cache import redis_client
from uuid import uuid4, UUID
from pydantic import BaseModel
from typing import Union


class InputFile(BaseModel):
    transcript_id: str
    filename: str
    transcription: str

class SummaryRequest(BaseModel):
    input_file: Union[InputFile, UploadFile]
    complexity: str
    locale: str

level = {
    "1": "You receive the transcription of an audio from a talk, conference, podcast or a text document. In both case, try to make a summarization with the most important information, be very concise, use some paragraphs but also bullet points.",
    "2":"You receive the transcription of an audio from a talk, conference, podcast or a text document. In both case, try to make a summarization with the most important information, be a little bit concise, use some paragraphs but also bullet points.",
    "3":"You receive the transcription of an audio from a talk, conference, podcast or a text document. In both case, try to make a summarization with the most important information, be wordy, use some paragraphs but also bullet points.",
    "4":"You receive the transcription of an audio from a talk, conference, podcast or a text document. In both case, try to make a summarization with the most important information be very wordy, use some paragraphs but also bullet points, all details must be there."
}


async def add_summary(input_file: SummaryRequest = Depends()):
    audio_data: InputFile={}
    audio_data.transcription = ""
    audio_data.transcript_id = uuid4()
    if input_file.content_type == "audio/mpeg":
        speech = await input_file.read()
        audio_data.transcription = __transcribe(speech)
        redis_client.json().set("transcript:{}".format(audio_data.transcript_id), Path.root_path(), {
            "fileName": input_file.filename,
            "data": audio_data.transcription
        })

    elif input_file.content_type == "text/plain":
        audio_data.transcription = await input_file.input_file.read()
        input_file.input_file = audio_data
    

    else:
        raise ValueError("File must have content type audio/mpeg or text/plain")
    

    summary = await __summarize(input_file.input_file.transcription, 
                                filename=input_file.input_file.filename, 
                                transcript_id=input_file.input_file.transcript_id,
                                complexity_value= input_file.complexity
                                )
    return summary


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


async def __summarize(transcription: str, filename: str = "", transcript_id: UUID = "", complexity_value: str = "1"):
    client = AsyncOpenAI(
        api_key=settings.openai_api_key
    )

    chat_completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": level[complexity_value]},
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
