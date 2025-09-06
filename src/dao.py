from dataclasses import dataclass
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0)


@dataclass
class Transcription:
    session_id: str
    text: str
    cashed: bool = False


def fetch_session_transcript(session_id: str) -> Transcription:
    """Fetches the entire transcript for a given session from Redis cache."""
    cached_item = redis_client.get(session_id)

    text = ""
    if cached_item:
        text = cached_item.decode("utf-8")

    return Transcription(session_id, text, cashed=True)


def save_session_chunk(session_id: str, chunk: str) -> Transcription:
    """Saves a chunk of transcript for a given session to Redis cache."""
    cached_item = redis_client.get(session_id)

    text = ""
    if cached_item:
        text = cached_item.decode("utf-8")

    text += chunk + " "

    # Store the item in Redis with an expiration time of 1 hour (3600 seconds)
    redis_client.setex(session_id, 3600, text)

    return Transcription(session_id, text, cashed=True)
