import json

import redis
from redis.commands.search.query import Query

from app import redis_cache
from app.models.cache import TranscriptModel


def add_transcript(uuid: str, transcript: TranscriptModel):
    return redis_cache.redis_client.set("transcript:{}".format(uuid), transcript.__str__())


def get_transcripts():
    for key in redis_cache.redis_client.keys("transcript:*"):
        yield {"transcript_id": key, "transcript": redis_cache.redis_client.json().get(key)}


def get_transcript(transcript_id: str):
    return redis_cache.redis_client.json().get("transcript:{}".format(transcript_id))
