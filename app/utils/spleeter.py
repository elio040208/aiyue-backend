import os
from typing import Optional
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter

separator = Separator('spleeter:2stems')
audio_adapter = AudioAdapter.default()

def separate_2stems(origin_path: str, vocal_path: str, accompaniment_path: str, sample_rate: Optional[int] = 44100) -> None:
    if not os.path.isfile(origin_path):
        raise FileNotFoundError(f"音频文件不存在: {origin_path}")

    waveform, _ = audio_adapter.load(origin_path, sample_rate=sample_rate)
    prediction = separator.separate(waveform)

    audio_adapter.save(vocal_path, prediction["vocals"], sample_rate, codec="wav")
    audio_adapter.save(accompaniment_path, prediction["accompaniment"], sample_rate, codec="wav")