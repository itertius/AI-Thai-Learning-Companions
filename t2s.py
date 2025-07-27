from gtts import gTTS
import os
import tempfile

def speak_thai(text):
    tts = gTTS(text, lang='th')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name