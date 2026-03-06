import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
print('Voces:', [v.id for v in voices])
engine.say('probando uno dos tres')
engine.runAndWait()
print('FIN - escuchaste algo?')