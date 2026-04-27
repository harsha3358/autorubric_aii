import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate(prompt: str):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 120,   # optimized
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)

        if response.status_code != 200:
            return "Model response unavailable."

        data = response.json()

        if isinstance(data, list):
            return data[0].get("generated_text", "").strip()

        return str(data)

    except Exception:
        return "Model timeout or connection issue."