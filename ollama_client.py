import json
import requests
from typing import List, Dict, Any, Optional

class OllamaClient:
    def __init__(self, host: str, model: str):
        self.host = host.rstrip("/")
        self.model = model

    def warmup(self):
        try:
            requests.post(
                f"{self.host}/api/chat",
                json={
                    "model": self.model,
                    "messages": [],
                    "keep_alive": "30m",
                    "stream": False,
                },
                timeout=30,
            )
        except Exception:
            pass

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "keep_alive": "30m",
            "options": {
                "temperature": 0.1
            }
        }
        if tools:
            payload["tools"] = tools

        resp = requests.post(f"{self.host}/api/chat", json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()["message"]
