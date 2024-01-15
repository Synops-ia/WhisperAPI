import torch
import uuid

from redis.commands.json.path import Path
from transformers import pipeline, AutoProcessor, WhisperForConditionalGeneration

from app.redis_cache import redis_client


async def speech_to_text(filename: str, payload, q):
    print('starting transcription')
    device = "cuda" if torch.cuda.is_available() else "cpu"
    checkpoint = "openai/whisper-small"
    model = WhisperForConditionalGeneration.from_pretrained(checkpoint)
    processor = AutoProcessor.from_pretrained(checkpoint)
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="french", task="transcribe")
    whisper_pipeline = pipeline("automatic-speech-recognition",
                                model=model,
                                tokenizer=processor.tokenizer,
                                feature_extractor=processor.feature_extractor,
                                generate_kwargs={
                                    # "forced_decoder_ids": forced_decoder_ids
                                },
                                chunk_length_s=30,
                                device=device
                                )
    transcript_id = q if q is not None else uuid.uuid4()
    speech = await payload.read()
    text = whisper_pipeline(speech)

    redis_client.json().set("transcript:{}".format(transcript_id), Path.root_path(), {
        "fileName": filename,
        "data": text
    })

    print('finished processing speech')

    return transcript_id, text
