# main.py
import tkinter as tk
from threading import Thread
import listener
from speech.tts import speak

# main.py

from listener import start_listener
import time

def on_sofi_activated():
    print("🌟 Sofi została wybudzona!")
    # Tu w przyszłości: odpal pełne rozpoznanie pytania, GUI, TTS itd.

if __name__ == "__main__":
    print("🚀 Uruchamiam Sofi...")
    start_listener(on_sofi_activated)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Zamykanie Sofi...")


is_listening = False

def on_wake():
    speak("Cześć Łukasz, słucham Cię 💗")
    # Tu potem aktywujemy Whisper do dalszego STT

def toggle_listening():
    global is_listening
    if not is_listening:
        is_listening = True
        button.config(text="⏹️ Zatrzymaj nasłuch")
        Thread(target=listener.listen_for_wake_word, args=(on_wake,), daemon=True).start()
    else:
        is_listening = False
        button.config(text="🎙️ Włącz nasłuch")
        # Można tu dodać zatrzymanie streamu

root = tk.Tk()
root.title("Sofi GUI")
button = tk.Button(root, text="🎙️ Włącz nasłuch", command=toggle_listening, width=25, height=2)
button.pack(padx=20, pady=20)
root.mainloop()
