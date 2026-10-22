"""Tiny Ollama client (stdlib only). Everything stays on your machine."""
import json
import os
import urllib.request

URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def available() -> bool:
    try:
        urllib.request.urlopen(URL + "/api/tags", timeout=1)
        return True
    except Exception:
        return False


def chat(messages: list) -> str:
    body = json.dumps({"model": MODEL, "messages": messages, "stream": False}).encode()
    req = urllib.request.Request(URL + "/api/chat", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["message"]["content"]
