import sounddevice as sd
import numpy as np
import queue
import threading
import time
import subprocess
import os
import config

# Import scipy z obsługą błędów
try:
    from scipy.io.wavfile import write
except ImportError:
    print("⚠️ Scipy nie jest zainstalowane. Używam alternatywnej metody zapisu audio.")
    import wave
    
    def write(filename, rate, data):
        """Alternatywna funkcja zapisu audio bez scipy"""
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(rate)
            wav_file.writeframes(data.tobytes())

# Globalne zmienne
audio_q = queue.Queue(maxsize=10)  # Ograniczenie rozmiaru kolejki
stop_threads = False
audio_buffer = []

def get_default_microphone():
    """Automatyczne wykrywanie najlepszego mikrofonu"""
    if config.MICROPHONE_DEVICE is not None:
        return config.MICROPHONE_DEVICE
    
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 6 and 'microphone' in device['name'].lower():
            print(f"🎤 Wykryto mikrofon: {device['name']} (ID: {i})")
            return i
    
    # Fallback - pierwszy dostępny mikrofon
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f"🎤 Używam mikrofonu: {device['name']} (ID: {i})")
            return i
    
    return None

def audio_callback(indata, frames, time_, status):
    """Callback do przechwytywania audio"""
    if status:
        print(f"{config.MESSAGES['mic_error']} {status}")
    
    # Sprawdź poziom głośności
    volume = np.sqrt(np.mean(indata**2))
    
    if volume > config.AUDIO_THRESHOLD:
        try:
            audio_q.put_nowait(indata.copy())
        except queue.Full:
            # Usuń najstarszy element jeśli kolejka pełna
            try:
                audio_q.get_nowait()
                audio_q.put_nowait(indata.copy())
            except queue.Empty:
                pass

def save_audio_clip(filename="wake_test.wav"):
    """Zapisz ostatnie sekundy audio do pliku"""
    if audio_q.empty():
        return False
    
    print(config.MESSAGES["processing"])
    frames = []
    
    # Zbierz wszystkie dostępne ramki
    while not audio_q.empty():
        try:
            data = audio_q.get_nowait()
            frames.append(data)
        except queue.Empty:
            break
    
    if not frames:
        return False
    
    # Połącz ramki audio
    audio = np.concatenate(frames, axis=0)
    
    # Konwertuj na mono jeśli stereo
    if len(audio.shape) > 1 and audio.shape[1] > 1:
        audio = audio[:, 0]
    
    # Normalizuj i konwertuj na int16
    audio = np.clip(audio, -1.0, 1.0)
    audio = np.int16(audio * 32767)
    
    # Zapisz do pliku
    try:
        write(filename, config.SAMPLE_RATE, audio)
        return True
    except Exception as e:
        print(f"{config.MESSAGES['mic_error']} {e}")
        return False

def whisper_transcribe(filepath):
    """Transkrypcja audio używając Whisper"""
    if not os.path.exists(filepath):
        return ""
    
    try:
        result = subprocess.run([
            config.WHISPER_EXE_PATH, 
            "-m", config.WHISPER_MODEL_PATH, 
            "-f", filepath, 
            "-otxt", "-nt", "-l", "pl"
        ], capture_output=True, text=True, timeout=10)
        
        # Sprawdź czy plik tekstowy został utworzony
        txt_file = filepath.replace('.wav', '.txt')
        if os.path.exists(txt_file):
            with open(txt_file, "r", encoding="utf8") as f:
                text = f.read().strip().lower()
            # Usuń plik tymczasowy
            try:
                os.remove(txt_file)
            except:
                pass
            return text
        
    except subprocess.TimeoutExpired:
        print("⏰ Timeout podczas transkrypcji")
    except Exception as e:
        print(f"{config.MESSAGES['transcript_error']} {e}")
    
    return ""

def listener_loop(on_activation_callback):
    """Główna pętla nasłuchiwania"""
    global stop_threads
    
    # Wykryj mikrofon
    mic_device = get_default_microphone()
    if mic_device is None:
        print("❌ Nie znaleziono mikrofonu!")
        return
    
    print(config.MESSAGES["mic_opening"])
    
    try:
        with sd.InputStream(
            device=mic_device, 
            channels=1, 
            samplerate=config.SAMPLE_RATE, 
            callback=audio_callback,
            blocksize=int(config.SAMPLE_RATE * 0.1)  # 100ms bloki
        ):
            print(config.MESSAGES["listening"])
            
            while not stop_threads:
                time.sleep(config.BLOCK_DURATION)
                
                if save_audio_clip():
                    transcript = whisper_transcribe("wake_test.wav")
                    
                    if transcript:
                        print(f"{config.MESSAGES['heard']} {transcript}")
                        
                        if config.WAKE_WORD in transcript:
                            print(config.MESSAGES["wake_detected"])
                            on_activation_callback()
                            time.sleep(2)  # Krótka pauza po aktywacji
                    else:
                        print(config.MESSAGES["no_speech"])
                
    except Exception as e:
        print(f"{config.MESSAGES['mic_error']} {e}")

def start_listener(on_activation_callback):
    """Uruchom nasłuchiwanie w osobnym wątku"""
    global stop_threads
    stop_threads = False
    
    # Wyczyść kolejkę audio
    while not audio_q.empty():
        try:
            audio_q.get_nowait()
        except queue.Empty:
            break
    
    t = threading.Thread(target=listener_loop, args=(on_activation_callback,))
    t.daemon = True
    t.start()
    return t

def stop_listener():
    """Zatrzymaj nasłuchiwanie"""
    global stop_threads
    stop_threads = True
