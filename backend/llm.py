import os
import requests

# 🔐 Get token from environment (Render)
HF_TOKEN = os.getenv("HF_TOKEN")

# ⚡ Faster model (you can switch if needed)
API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate(prompt: str):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 120,   # reduced for speed
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=8   # 🔥 prevents hanging
        )

        if response.status_code != 200:
            return "Model is temporarily unavailable."

        data = response.json()

        # Handle HF response format
        if isinstance(data, list):
            return data[0].get("generated_text", "").strip()

        return str(data)

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."

    except Exception:
        return "Model is busy. Try again shortly."