
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Local storage directory
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# AI configuration
MODEL_NAME = "qwen3:1.7b"

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

# Memory configuration
DATABASE_PATH = DATA_DIR / "memory.db"

MAX_HISTORY = 12

# Voice configuration
WHISPER_MODEL = "tiny.en"

VOICE_RATE = 170

# Application configuration
WINDOW_TITLE = "AI Companion"
