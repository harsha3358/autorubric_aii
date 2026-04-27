import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

# Primary model
HF_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def hf_generate(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 120,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    try:
        res = requests.post(HF_URL, headers=headers, json=payload, timeout=10)

        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list):
                return data[0].get("generated_text", "").strip()

    except:
        pass

    return None


# 🔥 FALLBACK (LOCAL LOGIC)
def fallback_response(prompt, answer):
    return f"""
Rubric:
- Covers key concepts
- Clear explanation
- Relevant to prompt

Feedback:
The answer addresses the topic but may lack depth or detailed explanation.
Try adding more examples and structured points.
"""


def generate(prompt):
    # Try HuggingFace first
    output = hf_generate(prompt)

    if output and len(output.strip()) > 20:
        return output

    # 🔥 fallback if model fails
    return fallback_response(prompt, prompt)