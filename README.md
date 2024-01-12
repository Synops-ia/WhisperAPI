# WhisperAPI

Build docker image:

> docker build -t whisperapi .

Run docker image:

> docker run --env-file .env -t --name whisper -p 8000:8000 whisperapi