import wave
from pathlib import Path


def get_wav_duration(file_path: Path) -> float:
    """ Returns the duration in seconds of the wav at file_path."""

    with wave.open(str(file_path.resolve()), 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
        return duration