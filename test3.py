# pip install gtts
from gtts import gTTS
import winsound
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import tempfile
import os
import time

def hablar(texto):
    print(f"[Jarvis]: {texto}")
    try:
        # Generar audio con gTTS
        tts = gTTS(text=texto, lang='es', slow=False)
        
        # Guardar en archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            temp_path = f.name
        tts.save(temp_path)
        
        # Reproducir con winsound (nativo de Windows, sin instalación)
        winsound.PlaySound(temp_path, winsound.SND_FILENAME)
        
        os.remove(temp_path)
        
    except Exception as e:
        print(f"[Error TTS]: {e}")

def escuchar():
    print("  Habla ahora...")
    audio_raw = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype='float32')
    sd.wait()
    
    audio_int16 = (audio_raw * 32767).astype(np.int16)
    audio = sr.AudioData(audio_int16.tobytes(), 16000, 2)
    
    r = sr.Recognizer()
    try:
        texto = r.recognize_google(audio, language='es-ES')
        return texto
    except sr.UnknownValueError:
        return None
    except Exception as e:
        print(f"[Error STT]: {e}")
        return None

# ── Test ──
hablar("hola esto es una prueba después de grabar")
print("Grabando...")
texto = escuchar()
if texto:
    print(f"Dijiste: {texto}")
    hablar(f"Dijiste: {texto}")
else:
    hablar("no entendí nada")
