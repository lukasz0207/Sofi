# listener.py
import queue
import sounddevice as sd
import vosk
import json

q = queue.Queue()

model = vosk.Model("models/vosk-model-small-pl-0.22")  # Ściągnij wcześniej
samplerate = 16000
device = None

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen_for_wake_word(callback_on_wake):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                           dtype='int16', channels=1, callback=audio_callback):
        print("⏳ Sofi nasłuchuje... Powiedz: Hej Sofi")

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                print("Rozpoznano:", text)
                if "sofi" in text.lower():
                    print("🎯 Słowo-klucz wykryte: Sofi")
                    callback_on_wake()
                    break  # przerwij po wykryciu
