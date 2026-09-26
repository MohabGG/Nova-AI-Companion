
# Nova - AI Companion

A locally hosted AI companion with a configurable personality,
persistent memory, voice interaction, and animated facial expressions.

## Current Version: v0.1.0 - Working Prototype

### Implemented Features
- Local LLM inference using Ollama and Qwen3 1.7B
- Python desktop application using PySide6
- Configurable personality
- Animated facial expressions
- Persistent SQLite memory
- Voice input using Faster-Whisper
- Offline speech synthesis
- Conversation history

### Known Limitations
- Speech recognition needs improvement
- Facial animations are currently basic
- Voice synthesis needs improvement
- Personality requires further customization
- AI response speed has not yet been optimized

## Technology Stack
- Python 3.12
- PySide6
- Ollama
- SQLite
- Faster-Whisper
- pyttsx3

## Getting Started

Install the Python dependencies:

    python -m pip install -r requirements.txt

Install Ollama and download the language model:

    ollama pull qwen3:1.7b

Launch the application:

    python main.py

## Development Roadmap

- [x] Local AI integration
- [x] Basic personality system
- [x] Persistent memory
- [x] Animated face
- [x] Voice input/output
- [ ] Improve speech recognition
- [ ] Upgrade language model
- [ ] Natural expressive voice
- [ ] Dynamic facial animations
- [ ] Advanced personality and memory
- [ ] Embedded hardware integration

## Privacy

Conversation history and personal memories are stored locally
and excluded from Git using .gitignore.
