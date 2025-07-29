import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import listener
from speech.tts import speak
import config
import time

# Globalne zmienne
is_listening = False
listener_thread = None
log_text = None

def log_message(message):
    """Dodaj wiadomość do logu"""
    if log_text:
        timestamp = time.strftime("%H:%M:%S")
        log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        log_text.see(tk.END)
        log_text.update()

def on_wake():
    """Callback wywoływany po wykryciu słowa aktywacyjnego"""
    message = "Cześć Łukasz, słucham Cię 💗"
    log_message(f"🎯 Aktywacja: {message}")
    speak(message)
    # Tu możesz dodać dalsze rozpoznawanie lub obsługę poleceń

def toggle_listening():
    """Przełącz nasłuchiwanie on/off"""
    global is_listening, listener_thread
    
    if not is_listening:
        is_listening = True
        button.config(text="⏹️ Zatrzymaj nasłuch", bg="#ff6b6b")
        status_label.config(text="🟢 Nasłuchiwanie aktywne", fg="green")
        log_message("🚀 Rozpoczynam nasłuchiwanie...")
        
        # Uruchom nasłuchiwanie
        listener_thread = listener.start_listener(on_wake)
        
    else:
        is_listening = False
        button.config(text="🎙️ Włącz nasłuch", bg="#4ecdc4")
        status_label.config(text="🔴 Nasłuchiwanie wyłączone", fg="red")
        log_message("⏹️ Zatrzymuję nasłuchiwanie...")
        
        # Zatrzymaj nasłuchiwanie
        listener.stop_listener()

def test_microphone():
    """Test mikrofonu"""
    log_message("🧪 Testowanie mikrofonu...")
    mic_device = listener.get_default_microphone()
    if mic_device is not None:
        log_message(f"✅ Mikrofon gotowy (ID: {mic_device})")
    else:
        log_message("❌ Nie znaleziono mikrofonu!")

def clear_log():
    """Wyczyść log"""
    if log_text:
        log_text.delete(1.0, tk.END)

def on_closing():
    """Obsługa zamykania aplikacji"""
    global is_listening
    if is_listening:
        listener.stop_listener()
    root.destroy()

# Tworzenie GUI
root = tk.Tk()
root.title("🤖 Sofi - Asystent Głosowy")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

# Protokół zamykania
root.protocol("WM_DELETE_WINDOW", on_closing)

# Nagłówek
header_frame = tk.Frame(root, bg="#2c3e50", height=60)
header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
header_frame.pack_propagate(False)

title_label = tk.Label(header_frame, text="🤖 SOFI - Asystent Głosowy", 
                      font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
title_label.pack(expand=True)

# Status
status_frame = tk.Frame(root, bg="#f0f0f0")
status_frame.pack(fill=tk.X, padx=10, pady=5)

status_label = tk.Label(status_frame, text="🔴 Nasłuchiwanie wyłączone", 
                       font=("Arial", 12), fg="red", bg="#f0f0f0")
status_label.pack()

wake_word_label = tk.Label(status_frame, text=f"💬 Słowo aktywacyjne: '{config.WAKE_WORD}'", 
                          font=("Arial", 10), fg="gray", bg="#f0f0f0")
wake_word_label.pack()

# Przyciski
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(fill=tk.X, padx=10, pady=10)

button = tk.Button(button_frame, text="🎙️ Włącz nasłuch", command=toggle_listening, 
                  width=20, height=2, font=("Arial", 12, "bold"), 
                  bg="#4ecdc4", fg="white", relief="raised")
button.pack(side=tk.LEFT, padx=(0, 10))

test_button = tk.Button(button_frame, text="🧪 Test mikrofonu", command=test_microphone,
                       width=15, height=2, font=("Arial", 10), 
                       bg="#95a5a6", fg="white", relief="raised")
test_button.pack(side=tk.LEFT, padx=(0, 10))

clear_button = tk.Button(button_frame, text="🗑️ Wyczyść log", command=clear_log,
                        width=12, height=2, font=("Arial", 10), 
                        bg="#e74c3c", fg="white", relief="raised")
clear_button.pack(side=tk.LEFT)

# Log
log_frame = tk.Frame(root, bg="#f0f0f0")
log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

log_label = tk.Label(log_frame, text="📋 Log aktywności:", 
                    font=("Arial", 10, "bold"), bg="#f0f0f0")
log_label.pack(anchor=tk.W)

log_text = scrolledtext.ScrolledText(log_frame, height=15, font=("Consolas", 9),
                                    bg="#2c3e50", fg="#ecf0f1", 
                                    insertbackground="white")
log_text.pack(fill=tk.BOTH, expand=True)

# Wiadomość powitalna
log_message("🎉 Sofi gotowa do pracy!")
log_message(f"⚙️ Słowo aktywacyjne: '{config.WAKE_WORD}'")
log_message("💡 Kliknij 'Włącz nasłuch' aby rozpocząć")

# Uruchom GUI
root.mainloop()
