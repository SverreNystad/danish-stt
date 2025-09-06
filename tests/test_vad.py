import pytest
from silero_vad import read_audio

from src.vad_service import get_vad_timestamps


@pytest.mark.slow
def test_vad_timestamps():
    """
    Test function for get_vad_timestamps.
    This function should be replaced with actual test logic.
    """
    wav = read_audio("tests/english-speech.mp3")
    timestamps = get_vad_timestamps(wav)
    assert isinstance(timestamps, list)
    assert len(timestamps) > 0
    assert all(isinstance(ts, dict) for ts in timestamps)
    assert all("start" in ts and "end" in ts for ts in timestamps)
    assert all(
        isinstance(ts["start"], float) and isinstance(ts["end"], float)
        for ts in timestamps
    )
    assert all(ts["start"] < ts["end"] for ts in timestamps)
