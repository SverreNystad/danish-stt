from dataclasses import dataclass
import secrets
import string
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


def create_session_id(
    ttl_seconds=3600, length=6, alphabet=string.digits, max_retries=50
):
    for _ in range(max_retries):
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        # SET key if not exists, with TTL. Using SET with NX and EX ensures atomicity and expiration
        ok = redis_client.set(code, "", ex=ttl_seconds, nx=True)
        if ok:
            return code
    raise RuntimeError("Exhausted retries; increase code length.")
