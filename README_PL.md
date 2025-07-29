# 🤖 SOFI - Asystent Głosowy

Inteligentny asystent głosowy z rozpoznawaniem polskich komend i słów aktywacyjnych.

## 🚀 Szybki Start

### 1. Diagnostyka systemu
```bash
python debug_sofi.py
```
Ten skrypt sprawdzi czy wszystko jest poprawnie skonfigurowane.

### 2. Test mikrofonu
```bash
python test_mikrofonu.py
```
Znajdzie najlepszy mikrofon i przetestuje jego działanie.

### 3. Uruchomienie Sofi
```bash
python main.py
```
Uruchomi główny interfejs z przyciskami i logiem aktywności.

## ⚙️ Konfiguracja

Wszystkie ustawienia znajdują się w pliku `config.py`:

```python
# Słowo aktywacyjne
WAKE_WORD = "cześć sofi"

# Mikrofon (None = automatyczne wykrywanie)
MICROPHONE_DEVICE = None

# Próg wykrywania głosu
AUDIO_THRESHOLD = 0.01
```

## 🎤 Rozwiązywanie Problemów

### Problem: Sofi nie słyszy mojego głosu

**Rozwiązanie:**
1. Uruchom `python test_mikrofonu.py`
2. Sprawdź czy mikrofon jest wykrywany
3. Przetestuj poziom głośności
4. Dostosuj `AUDIO_THRESHOLD` w config.py

### Problem: Słowo aktywacyjne nie działa

**Rozwiązanie:**
1. Sprawdź czy mówisz wyraźnie "cześć sofi"
2. Spróbuj zmienić `WAKE_WORD` na "hej sofi"
3. Sprawdź czy Whisper działa: `python debug_sofi.py`

### Problem: Błędy mikrofonu

**Rozwiązanie:**
1. Sprawdź listę mikrofonów: `python lista_mikrofonow.py`
2. Ustaw konkretny mikrofon w config.py: `MICROPHONE_DEVICE = 6`
3. Sprawdź uprawnienia do mikrofonu w systemie

### Problem: Whisper nie działa

**Rozwiązanie:**
1. Sprawdź ścieżki w config.py:
   - `WHISPER_EXE_PATH`
   - `WHISPER_MODEL_PATH`
2. Pobierz model: `ggml-base.bin` do folderu `models/`
3. Skompiluj Whisper jeśli potrzeba

## 📁 Struktura Plików

```
Sofi/
├── config.py           # Główna konfiguracja
├── main.py            # Interfejs GUI
├── listener.py        # Nasłuchiwanie głosu
├── debug_sofi.py      # Narzędzie diagnostyczne
├── test_mikrofonu.py  # Test mikrofonów
├── speech/
│   ├── tts.py         # Synteza mowy
│   └── stt_whisper.py # Rozpoznawanie mowy
├── whisper.cpp/       # Silnik Whisper
└── models/            # Modele AI
```

## 🔧 Zaawansowane Ustawienia

### Dostrajanie Mikrofonu
```python
# W config.py
MICROPHONE_DEVICE = 6        # ID konkretnego mikrofonu
AUDIO_THRESHOLD = 0.005      # Niższy próg = większa czułość
BLOCK_DURATION = 1           # Krótszy czas = szybsza reakcja
```

### Zmiana Słowa Aktywacyjnego
```python
# Przykłady słów aktywacyjnych
WAKE_WORD = "cześć sofi"     # Domyślne
WAKE_WORD = "hej sofi"       # Alternatywa
WAKE_WORD = "sofi"           # Krótkie
```

### Optymalizacja Wydajności
```python
# Dla słabszych komputerów
BLOCK_DURATION = 3           # Dłuższe bloki
AUDIO_THRESHOLD = 0.02       # Wyższy próg

# Dla mocniejszych komputerów  
BLOCK_DURATION = 1           # Krótsze bloki
AUDIO_THRESHOLD = 0.005      # Niższy próg
```

## 🐛 Debugowanie

### Logi w czasie rzeczywistym
Główny interfejs pokazuje wszystkie aktywności w oknie logu.

### Ręczne testowanie
```python
# Test konkretnego mikrofonu
from test_mikrofonu import test_microphone_volume
test_microphone_volume(6, duration=10)

# Test rozpoznawania
from listener import whisper_transcribe
result = whisper_transcribe("wake_test.wav")
print(result)
```

### Typowe Błędy

**"Nie znaleziono mikrofonu"**
- Sprawdź czy mikrofon jest podłączony
- Uruchom jako administrator
- Sprawdź sterowniki audio

**"Timeout podczas transkrypcji"**
- Whisper może być za wolny
- Sprawdź czy model istnieje
- Spróbuj mniejszego modelu

**"Błąd audio: Input overflowed"**
- Mikrofon może być za głośny
- Zmniejsz poziom mikrofonu w systemie
- Zwiększ `AUDIO_THRESHOLD`

## 💡 Wskazówki

1. **Mów wyraźnie** - Whisper lepiej rozpoznaje wyraźną mowę
2. **Unikaj hałasu** - Testuj w cichym otoczeniu
3. **Eksperymentuj** - Różne mikrofony mogą wymagać różnych ustawień
4. **Monitoruj logi** - Interfejs pokazuje co Sofi słyszy

## 🎯 Następne Kroki

Po uruchomieniu Sofi:

1. Kliknij "Test mikrofonu" aby sprawdzić audio
2. Kliknij "Włącz nasłuch" aby rozpocząć
3. Powiedz "cześć sofi" aby przetestować
4. Sprawdź logi czy Sofi Cię słyszy
5. Dostosuj ustawienia jeśli potrzeba

---

**Powodzenia z Sofi! 🎉**

Jeśli masz problemy, uruchom `debug_sofi.py` aby zdiagnozować system.
