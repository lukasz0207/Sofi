import sys
import os

print("🤖 SOFI 2.0 - SZYBKI TEST")
print("=" * 40)

# Test 1: Import modułów
print("\n1. 📦 Test importów:")
try:
    import sounddevice as sd
    print("   ✅ sounddevice")
except ImportError as e:
    print(f"   ❌ sounddevice: {e}")

try:
    import numpy as np
    print("   ✅ numpy")
except ImportError as e:
    print(f"   ❌ numpy: {e}")

try:
    import scipy
    print("   ✅ scipy")
except ImportError as e:
    print(f"   ❌ scipy: {e}")

try:
    import tkinter as tk
    print("   ✅ tkinter")
except ImportError as e:
    print(f"   ❌ tkinter: {e}")

try:
    import config
    print("   ✅ config")
    print(f"      Słowo aktywacyjne: '{config.WAKE_WORD}'")
    print(f"      Mikrofon: {config.MICROPHONE_DEVICE}")
    print(f"      Próg audio: {config.AUDIO_THRESHOLD}")
except ImportError as e:
    print(f"   ❌ config: {e}")

# Test 2: Mikrofony
print("\n2. 🎤 Test mikrofonów:")
try:
    import sounddevice as sd
    devices = sd.query_devices()
    input_devices = [d for d in devices if d['max_input_channels'] > 0]
    
    if input_devices:
        print(f"   ✅ Znaleziono {len(input_devices)} mikrofonów:")
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"      {i}: {device['name'][:50]}")
    else:
        print("   ❌ Nie znaleziono mikrofonów!")
        
except Exception as e:
    print(f"   ❌ Błąd: {e}")

# Test 3: Pliki Whisper
print("\n3. 🗣️ Test Whisper:")
try:
    import config
    exe_exists = os.path.exists(config.WHISPER_EXE_PATH)
    model_exists = os.path.exists(config.WHISPER_MODEL_PATH)
    
    print(f"   Whisper EXE: {'✅' if exe_exists else '❌'}")
    print(f"   Model: {'✅' if model_exists else '❌'}")
    
    if not exe_exists:
        print("   💡 Sprawdź ścieżkę do whisper-cli.exe")
    if not model_exists:
        print("   💡 Pobierz model ggml-base.bin")
        
except Exception as e:
    print(f"   ❌ Błąd: {e}")

# Test 4: Test prostego nagrywania
print("\n4. 🎙️ Test nagrywania (3 sekundy):")
try:
    import sounddevice as sd
    import numpy as np
    
    print("   🎤 Nagrywam 3 sekundy... Mów coś!")
    
    # Znajdź pierwszy dostępny mikrofon
    devices = sd.query_devices()
    mic_id = None
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            mic_id = i
            break
    
    if mic_id is not None:
        recording = sd.rec(int(3 * 16000), samplerate=16000, channels=1, device=mic_id)
        sd.wait()
        
        # Sprawdź poziom audio
        volume = np.sqrt(np.mean(recording**2))
        print(f"   📊 Poziom audio: {volume:.4f}")
        
        if volume > 0.001:
            print("   ✅ Mikrofon działa!")
            if volume > 0.01:
                print("   🔊 Dobry poziom głośności")
            else:
                print("   🔇 Niski poziom - mów głośniej")
        else:
            print("   ❌ Brak sygnału audio")
    else:
        print("   ❌ Nie znaleziono mikrofonu")
        
except Exception as e:
    print(f"   ❌ Błąd: {e}")

print("\n" + "=" * 40)
print("💡 Następne kroki:")
print("   1. Jeśli wszystko OK: python main.py")
print("   2. Jeśli problemy: sprawdź błędy powyżej")
print("   3. Dokumentacja: README_PL.md")

input("\n🔄 Naciśnij Enter aby zakończyć...")
