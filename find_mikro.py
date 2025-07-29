import sounddevice as sd

print("🎤 Wszystkie mikrofony:")
devices = sd.query_devices()

for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        name = device['name']
        print(f"{i}: {name}")
        
        # Sprawdź czy to Twój mikrofon
        if 'ten_mikro' in name.lower():
            print(f"   ⭐ TO JEST TWÓJ MIKROFON! ID: {i}")
