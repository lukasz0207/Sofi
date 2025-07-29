import os
import sys
import subprocess
import config
import sounddevice as sd

def check_dependencies():
    """Sprawdź czy wszystkie zależności są zainstalowane"""
    print("🔍 Sprawdzanie zależności...")
    
    required_modules = [
        'sounddevice', 'numpy', 'scipy', 'tkinter'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - BRAK")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️ Brakujące moduły: {', '.join(missing)}")
        print("💡 Zainstaluj je używając: pip install " + " ".join(missing))
        return False
    
    return True

def check_whisper_files():
    """Sprawdź czy pliki Whisper istnieją"""
    print("\n🔍 Sprawdzanie plików Whisper...")
    
    exe_exists = os.path.exists(config.WHISPER_EXE_PATH)
    model_exists = os.path.exists(config.WHISPER_MODEL_PATH)
    
    print(f"Whisper EXE: {'✅' if exe_exists else '❌'} {config.WHISPER_EXE_PATH}")
    print(f"Model: {'✅' if model_exists else '❌'} {config.WHISPER_MODEL_PATH}")
    
    if not exe_exists:
        print("💡 Skompiluj Whisper lub sprawdź ścieżkę w config.py")
    
    if not model_exists:
        print("💡 Pobierz model ggml-base.bin do folderu models/")
    
    return exe_exists and model_exists

def test_whisper():
    """Test działania Whisper"""
    print("\n🧪 Test Whisper...")
    
    if not check_whisper_files():
        return False
    
    # Sprawdź czy whisper odpowiada
    try:
        result = subprocess.run([
            config.WHISPER_EXE_PATH, "--help"
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Whisper odpowiada")
            return True
        else:
            print(f"❌ Whisper błąd: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Whisper timeout")
        return False
    except Exception as e:
        print(f"❌ Błąd Whisper: {e}")
        return False

def check_audio_devices():
    """Sprawdź urządzenia audio"""
    print("\n🔍 Sprawdzanie urządzeń audio...")
    
    try:
        devices = sd.query_devices()
        input_count = sum(1 for d in devices if d['max_input_channels'] > 0)
        
        print(f"📱 Znaleziono {input_count} urządzeń wejściowych")
        
        if input_count == 0:
            print("❌ Brak mikrofonów!")
            return False
        
        # Pokaż pierwsze 3 mikrofony
        print("🎤 Dostępne mikrofony:")
        count = 0
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0 and count < 3:
                print(f"   {i}: {device['name'][:50]}")
                count += 1
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd audio: {e}")
        return False

def check_config():
    """Sprawdź konfigurację"""
    print("\n🔍 Sprawdzanie konfiguracji...")
    
    print(f"Słowo aktywacyjne: '{config.WAKE_WORD}'")
    print(f"Częstotliwość: {config.SAMPLE_RATE}Hz")
    print(f"Czas bloku: {config.BLOCK_DURATION}s")
    print(f"Próg audio: {config.AUDIO_THRESHOLD}")
    print(f"Mikrofon: {config.MICROPHONE_DEVICE}")
    
    # Sprawdź czy słowo aktywacyjne nie jest za długie
    if len(config.WAKE_WORD.split()) > 3:
        print("⚠️ Słowo aktywacyjne może być za długie")
    
    # Sprawdź próg audio
    if config.AUDIO_THRESHOLD > 0.1:
        print("⚠️ Próg audio może być za wysoki")
    elif config.AUDIO_THRESHOLD < 0.001:
        print("⚠️ Próg audio może być za niski")
    
    return True

def run_quick_test():
    """Szybki test całego systemu"""
    print("\n🚀 SZYBKI TEST SYSTEMU")
    print("=" * 40)
    
    tests = [
        ("Zależności", check_dependencies),
        ("Pliki Whisper", check_whisper_files),
        ("Whisper", test_whisper),
        ("Audio", check_audio_devices),
        ("Konfiguracja", check_config)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Błąd w teście {name}: {e}")
            results.append((name, False))
    
    print("\n📊 PODSUMOWANIE:")
    print("-" * 30)
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:15} {status}")
        if not passed:
            all_passed = False
    
    print("-" * 30)
    if all_passed:
        print("🎉 Wszystkie testy przeszły! Sofi powinna działać.")
    else:
        print("⚠️ Niektóre testy nie przeszły. Sprawdź błędy powyżej.")
    
    return all_passed

def main():
    print("🤖 SOFI - NARZĘDZIE DIAGNOSTYCZNE")
    print("=" * 50)
    
    run_quick_test()
    
    print(f"\n💡 Następne kroki:")
    print("1. Uruchom test_mikrofonu.py aby przetestować mikrofon")
    print("2. Uruchom main.py aby uruchomić Sofi")
    print("3. Powiedz 'cześć sofi' aby przetestować rozpoznawanie")

if __name__ == "__main__":
    main()
