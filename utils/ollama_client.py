# utils/ollama_client.py
import requests

def query_ollama(prompt, model="llama3", stream=False):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": stream
            }
        )
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        return "⚠️ Failed to get a response from local model."
    except Exception as e:
        return f"⚠️ Ollama integration error: {str(e)}"
