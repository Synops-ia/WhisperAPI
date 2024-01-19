import redis
from redis import ResponseError
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
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
            prefix=["transcript:"], index_type=IndexType.JSON
        )
    )
