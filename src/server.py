from fastapi import FastAPI, WebSocket

from src.dao import create_session_id, fetch_session_transcript
from loguru import logger

app = FastAPI(
    title="The Transcription Microservice API",
    description="API that takes in audio and distributes transcriptions for sessions.",
    version="1.0.0",
)


# Hosting websocket
@app.websocket("/ws/host")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = create_session_id()
    await websocket.send_text(session_id)
    while True:
        data = await websocket.receive_bytes()
        logger.info(f"Received {len(data)} bytes")

        transcript = fetch_session_transcript(session_id)
        await websocket.send_text(transcript.text)


# Client websocket
@app.websocket("/ws/{session_id}")
async def websocket_client(websocket: WebSocket, session_id: str):
    await websocket.accept()
    while True:
        transcript = fetch_session_transcript(session_id)
        await websocket.send_text(transcript.text)
