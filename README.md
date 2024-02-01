# WhisperAPI

Build docker image:

> docker build -t whisperapi .

Run docker image:

> docker run --env-file .env -t --name whisper -p 8000:8000 whisperapi

Run translation image: 

```
$ docker run -dit -p 5000:5000 --name libretranslate libretranslate/libretranslate --load-only en,de,fr,ja
```

Run redis cache image:

```
$ docker run -dit -p 6379:6379 --name synopsia-redis redis/redis-stack-server:latest
```