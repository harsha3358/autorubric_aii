import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return "LLM Error"

    data = response.json()

    if isinstance(data, list):
        return data[0].get("generated_text", "")
    return str(data)