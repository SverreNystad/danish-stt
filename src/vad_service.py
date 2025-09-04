from silero_vad import load_silero_vad, get_speech_timestamps
from torch import Tensor


model = load_silero_vad()


def get_vad_timestamps(wav: Tensor) -> list[dict[str, float]]:
    """
    Get voice activity detection (VAD) timestamps from audio waveform.

    Args:
        wav (torch.Tensor): Audio waveform tensor.
    Returns:
        list[dict[str, float]]: List of dictionaries with 'start' and 'end' keys in seconds.

    Example:
        >>> from silero_vad import read_audio
        >>> wav = read_audio("tests/english-speech.mp3")
        >>> timestamps = get_vad_timestamps(wav)
        >>> print(timestamps)
        [{'start': 0.8, 'end': 2.5}, {'start': 2.8, 'end': 4.5}, {'start': 5.0, 'end': 7.0}, {'start': 7.3, 'end': 8.6}, {'start': 9.1, 'end': 10.5}, {'start': 11.3, 'end': 13.2}, {'start': 13.5, 'end': 14.5}, {'start': 14.8, 'end': 15.7}, {'start': 16.5, 'end': 18.1}, {'start': 18.3, 'end': 19.8}]

    """
    return get_speech_timestamps(
        wav,
        model,
        return_seconds=True,  # Return speech timestamps in seconds (default is samples)
    )
