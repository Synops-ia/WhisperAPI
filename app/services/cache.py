from app import redis_cache
from app.database.database import find_one_summary_in_db, find_all_summaries_in_db
from app.models.cache import TranscriptModel


def add_transcript(uuid: str, transcript: TranscriptModel):
    return redis_cache.redis_client.set("transcript:{}".format(uuid), transcript.__str__())


def get_transcripts():
    for key in redis_cache.redis_client.keys("transcript:*"):
        yield {"transcript_id": key, "transcript": redis_cache.redis_client.json().get(key)}


def get_transcript(transcript_id: str):
    return redis_cache.redis_client.json().get("transcript:{}".format(transcript_id))


def get_summary(transcript_id: str):
    if redis_cache.redis_client.json().get("summary:{}".format(transcript_id)) is None:
        return find_one_summary_in_db("summary:{}".format(transcript_id))
    return redis_cache.redis_client.json().get("summary:{}".format(transcript_id))


def get_summaries():
    keys = redis_cache.redis_client.keys("summary:*")

    if not keys:
        for summary in find_all_summaries_in_db():
            yield {"summary_id": summary["_id"], "summary": summary["summary"]}
    else:
        for key in keys:
            summary_data = redis_cache.redis_client.json().get(key)
            yield {"summary_id": key, "summary": summary_data}
