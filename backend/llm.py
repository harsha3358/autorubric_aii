import os
import requests
import json
import re

HF_TOKEN = os.getenv("HF_TOKEN")

# Primary model
HF_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
} if HF_TOKEN else {}

def generate_llm_metrics(prompt, answer):
    if not HF_TOKEN:
        return None

    evaluation_prompt = f"""[INST] You are an expert AI grader. Evaluate the student answer based on the assignment prompt.
You MUST respond ONLY with a valid JSON object. Do not include any markdown formatting, conversational text, or explanations outside the JSON object.

The JSON object MUST have exactly these 5 keys:
- "feedback": A short constructive feedback paragraph (string).
- "relevance": Score out of 100 (integer).
- "clarity": Score out of 100 (integer).
- "depth": Score out of 100 (integer).
- "structure": Score out of 100 (integer).

Prompt: {prompt}
Answer: {answer} [/INST]"""

    payload = {
        "inputs": evaluation_prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.1, # Low temperature for more deterministic JSON
            "return_full_text": False
        }
    }

    try:
        res = requests.post(HF_URL, headers=headers, json=payload, timeout=15)

        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list):
                raw_output = data[0].get("generated_text", "").strip()
                
                # Attempt to extract JSON if the LLM wrapped it in markdown code blocks
                json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                if json_match:
                    raw_output = json_match.group(0)
                
                parsed_data = json.loads(raw_output)
                return parsed_data
    except Exception as e:
        print(f"LLM Error: {e}")

    return None