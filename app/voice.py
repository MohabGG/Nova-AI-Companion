
import numpy as np
import sounddevice as sd

from app.config import WHISPER_MODEL, VOICE_RATE


_whisper = None


def record_and_transcribe():

    global _whisper

    sample_rate = 16000
    duration = 5

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    audio = np.asarray(audio).flatten()

    # Load Whisper only when the microphone is first used.
    if _whisper is None:

        from faster_whisper import WhisperModel

        _whisper = WhisperModel(
            WHISPER_MODEL,
            device="cpu",
            compute_type="int8"
        )

    segments, information = _whisper.transcribe(
        audio,
        language="en",
        beam_size=1
    )

    transcript = " ".join(
        segment.text.strip()
        for segment in segments
    )

    return transcript.strip()


def speak(text):

    import pyttsx3

    engine = pyttsx3.init()

    engine.setProperty(
        "rate",
        VOICE_RATE
    )

    engine.say(text)
    engine.runAndWait()
    engine.stop()
