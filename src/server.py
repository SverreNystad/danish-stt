from dataclasses import dataclass
import redis
from fastapi import FastAPI, WebSocket

app = FastAPI(
    title="The Transcription Microservice API",
    description="API that takes in audio and distributes transcriptions for sessions.",
    version="1.0.0",
)

redis_client = redis.Redis(host="localhost", port=6379, db=0)


@dataclass
class Transcription:
    session_id: str
    text: str
    cashed: bool = False


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    cached_item = redis_client.get(f"item_{item_id}")

    if cached_item:
        return {"item_id": item_id, "cached": True, "data": cached_item.decode("utf-8")}

    # Simulate data fetching process
    item_data = f"Item data for {item_id}"

    # Store the item in Redis with an expiration time of 1 hour (3600 seconds)
    redis_client.setex(f"item_{item_id}", 3600, item_data)

    return {"item_id": item_id, "cached": False, "data": item_data}


# Hosting websocket
@app.websocket("/ws/host")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        await websocket.send_text(f"Message text was: {data}")


# Client websocket
@app.websocket("/ws/{session_id}")
async def websocket_client(websocket: WebSocket, session_id: str):
    await websocket.accept()
    while True:
        transcript = fetch_session_transcript(session_id)
        await websocket.send_text(transcript.text)


def fetch_session_transcript(session_id: str):
    """Fetches the entire transcript for a given session from Redis cache."""
    cached_item = redis_client.get(session_id)

    text = ""
    if cached_item:
        text = cached_item.decode("utf-8")

    return Transcription(session_id, text, cashed=True)
