
import json
import requests

from app.config import MODEL_NAME, OLLAMA_URL
from app.personality import get_system_prompt


VALID_EMOTIONS = {
    "neutral",
    "happy",
    "curious",
    "concerned",
    "surprised"
}


class Brain:

    def __init__(self, memory):
        self.memory = memory

    def respond(self, user_message):

        system_prompt = get_system_prompt(
            self.memory.get_facts()
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages.extend(self.memory.get_history())

        messages.append({
            "role": "user",
            "content": user_message
        })

        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "format": "json",
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0.7
            }
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        raw_response = response.json()["message"]["content"]

        try:
            result = json.loads(raw_response)

            reply = str(result.get("reply", "")).strip()

            emotion = str(
                result.get("emotion", "neutral")
            ).lower().strip()

        except (json.JSONDecodeError, AttributeError, TypeError):
            reply = raw_response.strip()
            emotion = "neutral"

        if not reply:
            reply = "Sorry, I couldn't generate a response."

        if emotion not in VALID_EMOTIONS:
            emotion = "neutral"

        self.memory.save_exchange(
            user_message,
            reply
        )

        return reply, emotion
