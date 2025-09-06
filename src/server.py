from fastapi import FastAPI, WebSocket

from src.dao import create_session_id, fetch_session_transcript
from loguru import logger

app = FastAPI(
    title="The Transcription API",
    description="API for real-time transcription distributed to all clients in a session",
    version="1.0.0",
)


# Hosting websocket
@app.websocket("/ws/host")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = create_session_id()
    logger.info(f"Created session with id: {session_id}")
    await websocket.send_text(session_id)
    while True:
        data = await websocket.receive_bytes()
        logger.info(f"Received {len(data)} bytes")
        # TODO: Process audio data and update transcript in DB

        transcript = fetch_session_transcript(session_id)
        await websocket.send_text(transcript.text)
        logger.debug(f"Sent transcript: {transcript.text}")


# Client websocket
@app.websocket("/ws/{session_id}")
async def websocket_client(websocket: WebSocket, session_id: str):
    await websocket.accept()
    while True:
        transcript = fetch_session_transcript(session_id)
        await websocket.send_text(transcript.text)
