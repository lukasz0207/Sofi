from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig
from torch.serialization import add_safe_globals

# ✅ Powiedz PyTorchowi, że ufamy tym klasom
add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    BaseDatasetConfig,
    XttsArgs
])

# 🎤 Inicjalizacja modelu (na CPU)
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)

def speak(text: str):
    tts.tts_to_file(text=text, speaker_wav="sofi_voice.wav", file_path="sofi_output.wav")
