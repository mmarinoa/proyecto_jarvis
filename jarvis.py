# Dependencias necesarias:
# pip install gtts playsound==1.2.2 sounddevice speechrecognition numpy requests flask

from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import tempfile
import os
import time
import sys
import requests
import os

# ── Configuración ──────────────────────────────────────────
N8N_WEBHOOK_URL = "https://an8n.ilatina.es/webhook/jarvis"  
# ───────────────────────────────────────────────────────────


def hablar(texto):
    print(f"[Jarvis]: {texto}")
    try:
        tts = gTTS(text=texto, lang='es', slow=False)
        mp3_path = os.path.join(tempfile.gettempdir(), f"jarvis_{int(time.time()*1000)}.mp3")
        tts.save(mp3_path)

        wav_path = mp3_path.replace('.mp3', '.wav')
        try:
            from pydub import AudioSegment
            AudioSegment.from_mp3(mp3_path).export(wav_path, format="wav")
            import winsound
            winsound.PlaySound(wav_path, winsound.SND_FILENAME)
        except Exception as conv_err:
            print(f"No se pudo convertir a WAV ({conv_err}), usando playsound MP3")
            playsound(mp3_path)
        finally:
            if os.path.exists(mp3_path):
                os.remove(mp3_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)
    except Exception as e:
        print(f"[Error TTS]: {e}")


def escuchar(duracion=5):
    try:
        print("  [Escuchando...]")
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


def enviar_a_n8n(mensaje):
    """
    Envía el mensaje del usuario al webhook de n8n vía POST.
    Espera que n8n responda con un JSON: { "respuesta": "texto aquí" }
    """
    try:
        print(f"  [Enviando a n8n]: {mensaje}")
        payload = {"mensaje": mensaje}
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=15)
        response.raise_for_status()

        data = response.json()
        respuesta = data.get("respuesta", "")

        if respuesta:
            print(f"  [Respuesta de n8n]: {respuesta}")
            return respuesta
        else:
            print("  [n8n no devolvió 'respuesta' en el JSON]")
            return None

    except requests.exceptions.Timeout:
        print("  [Error]: Timeout esperando respuesta de n8n")
        return None
    except requests.exceptions.ConnectionError:
        print("  [Error]: No se pudo conectar con n8n. ¿Está corriendo el workflow?")
        return None
    except Exception as e:
        print(f"  [Error al contactar n8n]: {e}")
        return None


# ── Programa principal ──────────────────────────────────────
print("=" * 50)
print("       JARVIS - Asistente Virtual")
print("=" * 50)
print(f"  Webhook n8n: {N8N_WEBHOOK_URL}")
print("=" * 50)

hablar("Hola, soy Jarvis, tu asistente virtual. ¿En qué puedo ayudarte?")

try:
    while True:
        print("\n" + "-" * 40)
        time.sleep(0.3)

        texto_usuario = escuchar()

        if texto_usuario:
            print(f"  [Usuario]: {texto_usuario}")

            respuesta_n8n = enviar_a_n8n(texto_usuario)

            if respuesta_n8n:
                hablar(respuesta_n8n)
            else:
                hablar("Hubo un problema al procesar tu mensaje, inténtalo de nuevo.")
        else:
            hablar("No capté lo que dijiste, intenta de nuevo.")
            time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[Saliendo...]")
    hablar("Hasta luego")
    sys.exit(0)
