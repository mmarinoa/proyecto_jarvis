# servidor.py — Servidor HTTP que recibe respuestas de n8n y hace hablar a Jarvis
#
# Dependencias:
# pip install flask gtts playsound==1.2.2
#
# Uso: python servidor.py
# Corre en http://localhost:8765/respuesta
#
# En n8n: el último nodo HTTP Request hace POST a http://localhost:8765/respuesta
# con body JSON: { "respuesta": "El texto que debe decir Jarvis" }

from flask import Flask, request, jsonify
from gtts import gTTS
from playsound import playsound
import tempfile
import os
import time

app = Flask(__name__)


def hablar(texto):
    print(f"[Jarvis habla]: {texto}")
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
            print(f"Usando playsound MP3: {conv_err}")
            playsound(mp3_path)
        finally:
            if os.path.exists(mp3_path):
                os.remove(mp3_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)
    except Exception as e:
        print(f"[Error TTS]: {e}")


@app.route('/respuesta', methods=['POST'])
def recibir_respuesta():
    """
    Endpoint que n8n llama con POST.
    Body esperado (JSON): { "respuesta": "texto que dirá Jarvis" }
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Body JSON vacío o inválido"}), 400

    texto = data.get("respuesta", "").strip()

    if not texto:
        return jsonify({"error": "Campo 'respuesta' vacío o no encontrado"}), 400

    print(f"[Recibido de n8n]: {texto}")
    hablar(texto)

    return jsonify({"status": "ok", "texto_dicho": texto}), 200


@app.route('/ping', methods=['GET'])
def ping():
    """Endpoint de prueba para verificar que el servidor está vivo."""
    return jsonify({"status": "Jarvis servidor activo"}), 200


if __name__ == '__main__':
    print("=" * 50)
    print("  Servidor Jarvis escuchando en puerto 8765")
    print("  Endpoint: POST http://localhost:8765/respuesta")
    print("  Prueba:   GET  http://localhost:8765/ping")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8765, debug=False)