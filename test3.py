# Dependencias necesarias:
# pip install gtts playsound==1.2.2 sounddevice speechrecognition numpy

from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import tempfile
import os
import time
import sys

def hablar(texto):
    print(f"[Jarvis]: {texto}")
    try:

        
        # Generar audio con gTTS
        tts = gTTS(text=texto, lang='es', slow=False)

        # Guardar en archivo temporal mp3
        mp3_path = os.path.join(tempfile.gettempdir(), f"jarvis_{int(time.time()*1000)}.mp3")
        tts.save(mp3_path)

        # intentamos convertir a WAV para evitar problemas de codec de MP3 en Windows
        wav_path = mp3_path.replace('.mp3', '.wav')
        try:
            from pydub import AudioSegment
            AudioSegment.from_mp3(mp3_path).export(wav_path, format="wav")
            # reproducir WAV usando winsound (nativo y ligero)
            import winsound
            winsound.PlaySound(wav_path, winsound.SND_FILENAME)
        except Exception as conv_err:
            # si falla la conversión -> prueba playsound con el MP3
            print(f"No se pudo convertir a WAV ({conv_err}), usando playsound MP3")
            from playsound import playsound
            playsound(mp3_path)
        finally:
            # limpiar archivos
            if os.path.exists(mp3_path):
                os.remove(mp3_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)
    except Exception as e:
        print(f"[Error TTS]: {e}")


def escuchar(duracion=5):
    try:
        audio_raw = sd.rec(
            int(duracion * 16000),
            samplerate=16000,
            channels=1,
            dtype='float32'
        )
        sd.wait()

        audio_int16 = (audio_raw * 32767).astype(np.int16)
        audio = sr.AudioData(audio_int16.tobytes(), 16000, 2)

        r = sr.Recognizer()
        texto = r.recognize_google(audio, language='es-ES')
        return texto

    except sr.UnknownValueError:
        print("  No te entendí, intenta de nuevo")
        return None
    except sr.RequestError as e:
        print(f"  Error de conexión con Google: {e}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

# ── Programa principal ──
print("=" * 50)
print("       JARVIS - Asistente Virtual")
print("=" * 50)

hablar("Hola, soy Jarvis, tu asistente virtual")

try:
    while True:
        print("\n" + "-" * 40)
        hablar("Por favor, habla algo")
        time.sleep(0.3)

        texto = escuchar()

        if texto:
            print(f"  Dijiste: {texto}")
            hablar(f"Dijiste: {texto}")
        else:
            hablar("No capté lo que dijiste, intenta de nuevo")
            time.sleep(0.5)
        # time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[Saliendo...]")
    hablar("Hasta luego")
    sys.exit(0)