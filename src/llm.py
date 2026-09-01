import json
import os
import requests

def ollama_available(base="http://localhost:11434"):
    try:
        return requests.get(base + "/api/tags", timeout=1.5).ok
    except Exception:
        return False

def generate_local(prompt, model="llama3.2:3b", base="http://localhost:11434",
                    num_predict=140, num_ctx=1024, keep_alive="30m"):
    """Non-streaming call. Kept for callers (e.g. fallback paths, tests)
    that just want the final string."""
    r = requests.post(base + "/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": keep_alive,           # keeps model loaded in RAM -> no cold-start delay
            "options": {
                "num_predict": num_predict,     # shorter answer -> faster finish
                "num_ctx": num_ctx,             # smaller context window -> less to process
                "num_thread": os.cpu_count() or 4,  # use all logical CPU cores
            },
        }, timeout=120)
    r.raise_for_status()
    return r.json().get("response", "").strip()

def generate_local_stream(prompt, model="llama3.2:3b", base="http://localhost:11434",
                           num_predict=140, num_ctx=1024, keep_alive="30m"):
    """Streaming call. Yields text chunks as the model produces them, so the
    UI can show tokens live (like ChatGPT/Claude) instead of waiting for the
    full answer."""
    r = requests.post(base + "/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": True,
            "keep_alive": keep_alive,
            "options": {
                "num_predict": num_predict,
                "num_ctx": num_ctx,
                "num_thread": os.cpu_count() or 4,
            },
        }, stream=True, timeout=120)
    r.raise_for_status()
    for line in r.iter_lines():
        if not line:
            continue
        chunk = json.loads(line)
        piece = chunk.get("response", "")
        if piece:
            yield piece
        if chunk.get("done"):
            break
