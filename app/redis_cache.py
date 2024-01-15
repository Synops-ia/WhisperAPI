import redis
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
schema = (
    TextField("$.fileName", as_name="fileName"),
    TextField("$.data", as_name="data"),
)
redis_search = redis_client.ft("idx:transcripts")
redis_search.dropindex("transcripts")
redis_search.create_index(
    schema,
    definition=IndexDefinition(
        prefix=["transcript:"], index_type=IndexType.JSON
    )
)
