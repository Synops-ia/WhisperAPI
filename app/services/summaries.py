from fastapi import File, UploadFile
import torch
from transformers import pipeline, AutoProcessor, WhisperForConditionalGeneration
from openai import AsyncOpenAI
from ..config import settings



async def add_summary(input_file: UploadFile = File(...)):
    transcription = ""
    if input_file.content_type == "audio/mpeg":
        speech = await input_file.read()
        transcription = __transcribe(speech)
    elif input_file.content_type == "text/plain":
        transcription = input_file.read()
    else:
        raise ValueError("File must have content type audio/mpeg or text/plain")
    
    summary = await __summarize(transcription)
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

async def __summarize(transcription: str):
    client = AsyncOpenAI(
        api_key=settings.openai_api_key
    )

    chat_completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You receive the transcription of an audio from a talk, conference, podcast. Try to make a summarization with the most important information, use some paragraphs but also bullet points."},
            {"role": "user", "content": transcription}
        ],
        max_tokens=1000
    )
    summary = chat_completion.choices[0].message.content
    return summary

