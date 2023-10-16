import base64
import threading
from io import BytesIO
from threading import Lock

import streamlit as st

from gtts import gTTS

class AudioBytes:
    bytes_io: BytesIO
    base_64_bytes: bytes

    def __init__(self, bytes_io: BytesIO):
        self.bytes_io = bytes_io
        self.builtin_bytes = base64.b64encode(bytes_io.getvalue()).decode()

class AudioCache:
    audio_bytes: dict[str, AudioBytes]
    lock: Lock

    def __init__(self):
        self.audio_bytes = {}
        self.lock = threading.Lock()
        print("Created Audio Cache!")

    def get_text_audio(self, text: str) -> AudioBytes:
        with self.lock:
            if text in self.audio_bytes:
                print("Audio cache hit: " + text[:10])
                return self.audio_bytes[text]
            else:
                print("Audio cache miss: " + text[:10])
                text_audio = self._load_audio(text)
                self.audio_bytes[text] = text_audio
                return text_audio

    def _load_audio(self, text: str) -> AudioBytes:
        # get audio from server
        tts = gTTS(text=text, lang="en")

        # convert to file-like object
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return AudioBytes(fp)

@st.cache_resource
def get_audio_cache() -> AudioCache:
    return AudioCache()
