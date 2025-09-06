from fastapi import FastAPI, WebSocket

from src.dao import fetch_session_transcript

app = FastAPI(
    title="The Transcription Microservice API",
    description="API that takes in audio and distributes transcriptions for sessions.",
    version="1.0.0",
)


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
