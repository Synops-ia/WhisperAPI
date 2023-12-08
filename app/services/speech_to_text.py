import torch
from transformers import pipeline, AutoProcessor, WhisperForConditionalGeneration


async def speech_to_text(speech_file):
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
                                    #"forced_decoder_ids": forced_decoder_ids
                                },
                                chunk_length_s=30,
                                device=device
    )
    speech = await speech_file.read()
    text = whisper_pipeline(speech)

    return text
