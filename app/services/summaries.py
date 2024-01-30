from fastapi import File, UploadFile
import torch
from redis.commands.json.path import Path
from transformers import pipeline, AutoProcessor, WhisperForConditionalGeneration
from openai import AsyncOpenAI
from ..config import settings
from ..redis_cache import redis_client
from uuid import uuid4, UUID
from .cache import get_transcript, get_summary

level = {
    "1": "very concise",
    "2": "little bit concise",
    "3": "wordy, but with only the most important information,",
    "4": "wordy and very detailed"
}

language = {
    "en": "english",
    "fr": "french"
}


async def add_summary(input_file: UploadFile = File(...), complexity: str = "1", locale: str = "en", transcript_id: str="") -> str:
    transcription = ""
    
    if input_file.content_type == "audio/mpeg":
        speech = await input_file.read()
        transcription = __transcribe(speech)
        redis_client.json().set("transcript:{}".format(transcript_id), Path.root_path(), {
            "fileName": input_file.filename,
            "data": transcription,
            "in_process": "0"
        })

    elif input_file.content_type == "text/plain":
        transcription = input_file.read()
    else:
        raise ValueError("File must have content type audio/mpeg or text/plain")
    
    redis_client.json().set("summary:{}".format(transcript_id), Path.root_path(), {
        "fileName": input_file.filename,
        "data": transcription,
        "in_process": "1"
    })
    await __summarize(transcription, filename=input_file.filename, transcript_id=transcript_id,
                                complexity=complexity, locale=locale)
    


async def retry_summary(transcript_id, complexity, locale):
    document = get_summary(transcript_id)
    redis_client.json().set("transcript:{}".format(transcript_id), Path.root_path(), {
            "fileName": document.filename,
            "data": document.data,
            "in_process": "1"
    })
    transcription = get_transcript(transcript_id)
    await __summarize(transcription["data"], transcription["fileName"], transcript_id, complexity, locale)


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


async def __summarize(transcription: str, filename: str = "", transcript_id: UUID = "", complexity: str = "1",
                      locale: str = "en"):
    client = AsyncOpenAI(
        api_key=settings.openai_api_key
    )

    chat_completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"you are a useful assistant that can generate a {level[complexity]} yet comprehensive summarization that "
                        "distills crucial insights for quick comprehension. Utilize a combination of well-crafted "
                        "paragraphs and bullet points to enhance visual hierarchy. you use titles when necessary to "
                        "have a well organized summary. you always output in HTML : title's should be <h1> tags, subtitles h2, list will be <ol> and <li> tags (for these ones, you will have to overwrite the default styling classes with tailwind), you will put important information in bold (<b />, italic <i /> or underlined <u />. you can use tailwind classes to style the summary as necessary."
                        f"you will also output in the following language: {language[locale]}"
             },
            {"role": "user", "content": transcription}
        ],
        max_tokens=1000
    )
    summary = chat_completion.choices[0].message.content
    redis_client.json().set("summary:{}".format(transcript_id), Path.root_path(), {
        "fileName": filename,
        "data": summary,
        "in_process": "0"
    })
