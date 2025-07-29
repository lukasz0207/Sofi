# config.py

# Ustawienia głosu i TTS
VOICE_SAMPLE_PATH = "assets/voice.wav"
XTTS_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
LANGUAGE = "pl"
USE_CUDA = True  # Użyj GPU, jeśli masz np. RX 580

# Ustawienia nasłuchiwania
WAKE_WORD = "cześć sofi"  # Ujednolicone słowo aktywacyjne
MICROPHONE_DEVICE = None  # None = automatyczne wykrywanie, lub podaj numer urządzenia
SAMPLE_RATE = 16000
BLOCK_DURATION = 2  # Skrócone do 2 sekund dla lepszej responsywności
AUDIO_THRESHOLD = 0.01  # Próg głośności do wykrywania mowy

# Ścieżki do Whisper
WHISPER_EXE_PATH = r"C:\Users\lukil\Desktop\Sofi\whisper.cpp\bindings\build\bin\Release\whisper-cli.exe"
WHISPER_MODEL_PATH = r"C:\Users\lukil\Desktop\Sofi\whisper.cpp\models\ggml-base.bin"

# Komunikaty po polsku
MESSAGES = {
    "listening": "👂 Sofi nasłuchuje...",
    "heard": "🗣️ Usłyszane:",
    "wake_detected": "💡 Hasło aktywacyjne rozpoznane!",
    "mic_error": "❌ Błąd mikrofonu:",
    "transcript_error": "❌ Błąd odczytu transkryptu:",
    "mic_opening": "🎤 Próba otwarcia mikrofonu...",
    "recording": "🎙️ Nagrywam...",
    "processing": "🔄 Przetwarzam audio...",
    "no_speech": "🔇 Nie wykryto mowy"
}
