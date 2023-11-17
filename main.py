from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from transformers import pipeline, AutoProcessor, WhisperForConditionalGeneration

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# Initialisation du pipeline Whisper
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
)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    # Vérifiez et lisez le fichier audio
    contents = await file.read()

    # Exécutez l'inférence Whisper
    transcription = whisper_pipeline(contents)

    return {"transcription": transcription}
