import sounddevice as sd
import numpy as np
import time
import config

def list_microphones():
    """Wyświetl listę dostępnych mikrofonów"""
    print("🎤 Dostępne urządzenia audio:")
    print("-" * 60)
    
    devices = sd.query_devices()
    input_devices = []
    
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            input_devices.append((i, device))
            status = "✅ ZALECANY" if 'microphone' in device['name'].lower() else "📱 Dostępny"
            print(f"{i:2d}: {device['name'][:40]:40} | {status}")
            print(f"    Kanały: {device['max_input_channels']}, Częstotliwość: {device['default_samplerate']:.0f}Hz")
    
    print("-" * 60)
    return input_devices

def test_microphone_volume(device_id, duration=5):
    """Test poziomu głośności mikrofonu"""
    print(f"\n🧪 Testowanie mikrofonu ID {device_id} przez {duration} sekund...")
    print("💬 Mów coś do mikrofonu...")
    
    volumes = []
    
    def audio_callback(indata, frames, time, status):
        if status:
            print(f"⚠️ Status: {status}")
        volume = np.sqrt(np.mean(indata**2))
        volumes.append(volume)
    
    try:
        with sd.InputStream(device=device_id, channels=1, 
                           samplerate=config.SAMPLE_RATE, 
                           callback=audio_callback):
            
            for i in range(duration):
                time.sleep(1)
                if volumes:
                    current_vol = volumes[-1]
                    bar_length = int(current_vol * 50)
                    bar = "█" * bar_length + "░" * (50 - bar_length)
                    print(f"\r🔊 [{bar}] {current_vol:.4f}", end="", flush=True)
            
            print()  # Nowa linia
            
            if volumes:
                avg_volume = np.mean(volumes)
                max_volume = np.max(volumes)
                
                print(f"\n📊 Wyniki testu:")
                print(f"   Średni poziom: {avg_volume:.4f}")
                print(f"   Maksymalny poziom: {max_volume:.4f}")
                print(f"   Próg wykrywania: {config.AUDIO_THRESHOLD}")
                
                if max_volume > config.AUDIO_THRESHOLD:
                    print("✅ Mikrofon działa poprawnie!")
                    return True
                else:
                    print("⚠️ Poziom audio może być za niski")
                    print(f"💡 Spróbuj mówić głośniej lub zmień próg na {max_volume * 0.5:.4f}")
                    return False
            else:
                print("❌ Nie wykryto żadnego audio")
                return False
                
    except Exception as e:
        print(f"❌ Błąd podczas testowania: {e}")
        return False

def auto_detect_best_microphone():
    """Automatyczne wykrywanie najlepszego mikrofonu"""
    print("\n🔍 Automatyczne wykrywanie najlepszego mikrofonu...")
    
    devices = sd.query_devices()
    candidates = []
    
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            score = 0
            name_lower = device['name'].lower()
            
            # Punktacja na podstawie nazwy
            if 'microphone' in name_lower:
                score += 10
            if 'usb' in name_lower:
                score += 5
            if 'headset' in name_lower:
                score += 3
            if 'webcam' in name_lower:
                score += 2
            
            # Punktacja na podstawie parametrów
            if device['default_samplerate'] >= 16000:
                score += 2
            if device['max_input_channels'] == 1:
                score += 1
                
            candidates.append((i, device, score))
    
    # Sortuj według punktacji
    candidates.sort(key=lambda x: x[2], reverse=True)
    
    print("🏆 Ranking mikrofonów:")
    for i, (device_id, device, score) in enumerate(candidates[:5]):
        print(f"{i+1}. ID {device_id}: {device['name'][:40]} (punkty: {score})")
    
    if candidates:
        best_id = candidates[0][0]
        print(f"\n💡 Zalecany mikrofon: ID {best_id}")
        return best_id
    
    return None

def main():
    """Główna funkcja testowa"""
    print("🎤 TESTER MIKROFONÓW SOFI")
    print("=" * 50)
    
    # Lista mikrofonów
    input_devices = list_microphones()
    
    if not input_devices:
        print("❌ Nie znaleziono mikrofonów!")
        return
    
    # Automatyczne wykrywanie
    best_mic = auto_detect_best_microphone()
    
    # Test wybranego mikrofonu
    if best_mic is not None:
        print(f"\n🧪 Testowanie zalecanego mikrofonu (ID {best_mic})...")
        success = test_microphone_volume(best_mic)
        
        if success:
            print(f"\n✅ Zalecenie: Ustaw MICROPHONE_DEVICE = {best_mic} w config.py")
        else:
            print(f"\n⚠️ Mikrofon ID {best_mic} może wymagać dostrojenia")
    
    # Opcja manualnego testowania
    print(f"\n💡 Aby przetestować inny mikrofon, uruchom:")
    print(f"   test_microphone_volume(ID_MIKROFONU)")

if __name__ == "__main__":
    main()
