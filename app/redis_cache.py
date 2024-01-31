import redis
from redis import ResponseError
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

from app.database.database import insert_summary_in_db

shadow_key = "shadowKey:"


def expire_handler(message):
    try:
        key = message['data']
        if shadow_key in key:
            key = key.replace(shadow_key, "")

            if "transcript:" in key:
                redis_client.delete(key)
            else:
                summary = redis_client.json().get(key)
                redis_client.delete(key)
                insert_summary_in_db(key, summary)
    except Exception as e:
        print(e)


redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

pub_sub = redis_client.pubsub()
pub_sub.subscribe(**{'__keyevent@0__:expired': expire_handler})
pub_sub.run_in_thread(sleep_time=0.01)

schema = (
    TextField("$.fileName", as_name="fileName"),
    TextField("$.data", as_name="data"),
)
summary_schema = (
    TextField("$.fileName", as_name="fileName"),
    TextField("$.data", as_name="data"),
)
redis_search = redis_client.ft("idx:transcripts")
summary_redis_search = redis_client.ft("idx:summaries")

try:
    redis_search.info()
except ResponseError:
    redis_search.create_index(
        schema,
        definition=IndexDefinition(
            prefix=["transcript:"], index_type=IndexType.JSON
        )
    )

try:
    summary_redis_search.info()
except ResponseError:
    summary_redis_search.create_index(
        summary_schema,
        definition=IndexDefinition(
            prefix=["summary:"], index_type=IndexType.JSON
        )
    )
