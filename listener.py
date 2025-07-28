# listener.py

import sounddevice as sd
import numpy as np
import queue
import threading
import time
import subprocess
import os

WAKE_WORD = "hej sofi"
SAMPLE_RATE = 16000
BLOCK_DURATION = 1  # sekundy

audio_q = queue.Queue()

listening = False
stop_threads = False

def audio_callback(indata, frames, time_, status):
    if status:
        print("Błąd audio:", status)
    audio_q.put(indata.copy())

def save_audio_clip(filename="wake_test.wav", duration=1):
    frames = []
    for _ in range(int(duration / BLOCK_DURATION)):
        data = audio_q.get()
        frames.append(data)
    audio = np.concatenate(frames, axis=0)
    audio = audio[:, 0]  # mono
    audio = np.int16(audio * 32767)
    from scipy.io.wavfile import write
    write(filename, SAMPLE_RATE, audio)

def whisper_transcribe(filepath):
    exe_path = r"C:\Users\lukil\Desktop\Sofi\whisper.cpp\build\bin\Release\main.exe"
    model_path = r"C:\Users\lukil\Desktop\Sofi\whisper.cpp\models\ggml-base.en.bin"
    result = subprocess.run([
        exe_path, "-m", model_path, "-f", filepath, "-otxt", "-nt"
    ], capture_output=True)
    try:
        with open("wake_test.wav.txt", "r", encoding="utf8") as f:
            text = f.read().strip().lower()
        return text
    except Exception as e:
        print("Błąd odczytu transkryptu:", e)
        return ""

def listener_loop(on_activation_callback):
    global listening
    with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, callback=audio_callback):
        print("👂 Sofi nasłuchuje...")
        while not stop_threads:
            save_audio_clip()
            transcript = whisper_transcribe("wake_test.wav")
            print("🗣️ Usłyszane:", transcript)
            if WAKE_WORD in transcript:
                print("💡 Hasło aktywacyjne rozpoznane!")
                on_activation_callback()
                time.sleep(1)

def start_listener(on_activation_callback):
    t = threading.Thread(target=listener_loop, args=(on_activation_callback,))
    t.daemon = True
    t.start()
