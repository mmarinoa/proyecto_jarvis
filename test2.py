import pyttsx3
import speech_recognition as sr
import sounddevice as sd
import numpy as np

engine = pyttsx3.init()

# Paso 1: habla ANTES de grabar
engine.say("voy a escucharte ahora")
engine.runAndWait()
print("Habla algo...")

# Paso 2: graba
audio_raw = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype='float32')
sd.wait()
print("Grabacion terminada")

# Paso 3: reconoce
audio_int16 = (audio_raw * 32767).astype(np.int16)
audio = sr.AudioData(audio_int16.tobytes(), 16000, 2)
r = sr.Recognizer()
try:
    texto = r.recognize_google(audio, language='es-ES')
    print(f"Dijiste: {texto}")
except:
    print("No entendi nada")

# Paso 4: habla DESPUÉS de que sounddevice terminó del todo
import time
time.sleep(1)
engine.say(f"repetire lo que dijiste")
engine.runAndWait()
print("FIN")