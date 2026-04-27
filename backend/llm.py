import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

# Primary model
HF_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
} if HF_TOKEN else {}

def hf_generate(prompt, answer):
    if not HF_TOKEN:
        return None

    evaluation_prompt = f"[INST] You are an expert AI grader. Evaluate the following student answer based on the assignment prompt. Provide a short constructive feedback paragraph and a Markdown table rubric scoring Clarity, Depth, and Relevance out of 100.\n\nPrompt: {prompt}\nAnswer: {answer} [/INST]"

    payload = {
        "inputs": evaluation_prompt,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.3,
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

# FALLBACK (LOCAL LOGIC)
def fallback_response(prompt, answer, score):
    if score >= 80:
        feedback = "Excellent response with strong clarity, depth, and relevance."
    elif score >= 50:
        feedback = "Good answer with solid understanding, but could benefit from deeper explanation."
    else:
        feedback = "Weak response. Lacks clarity, depth, and alignment with the prompt."

    rubric = f"""
### Evaluation Rubric

| Criteria | Score | Notes |
| :--- | :--- | :--- |
| **Relevance** | Calculated | Based on keyword overlap with the prompt |
| **Depth** | Calculated | Based on the length and detail of the answer |
| **Structure** | Calculated | Based on sentence formation and paragraphing |
| **Clarity** | Calculated | Based on vocabulary and readability |

*Note: This rubric was generated using statistical analysis because the AI grading service is currently unavailable.*
"""
    return feedback, rubric


def generate(prompt, answer, score):
    # Try HuggingFace first
    output = hf_generate(prompt, answer)

    if output and len(output.strip()) > 20:
        # If output is generated, we'll try to split it or just return it as rubric
        return "AI Generated Feedback", output

    # fallback if model fails or HF_TOKEN is missing
    return fallback_response(prompt, answer, score)