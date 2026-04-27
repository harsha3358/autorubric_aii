import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate(prompt: str):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 120,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=8
        )

        if response.status_code != 200:
            return "Model is temporarily unavailable."

        data = response.json()

        if isinstance(data, list):
            return data[0].get("generated_text", "").strip()

        return str(data)

    except requests.exceptions.Timeout:
        return "Request timed out. Try again."

    except Exception:
        return "Model is busy. Try later."