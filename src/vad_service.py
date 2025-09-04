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
        >>> wav = read_audio("english-speech.mp3")
        >>> timestamps = get_vad_timestamps(wav)
        >>> print(timestamps)
        [{'start': 0.8, 'end': 2.5}, {'start': 2.8, 'end': 4.5}, {'start': 5.0, 'end': 7.0}, {'start': 7.3, 'end': 8.6}]

    """
    return get_speech_timestamps(
        wav,
        model,
        return_seconds=True,  # Return speech timestamps in seconds (default is samples)
    )
