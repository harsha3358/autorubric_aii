from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_score(a, b):
    v1 = model.encode(a)
    v2 = model.encode(b)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def length_score(answer):
    words = len(answer.split())
    if words > 80:
        return 1.0
    elif words > 40:
        return 0.7
    elif words > 20:
        return 0.4
    else:
        return 0.1

def keyword_score(prompt, answer):
    prompt_words = set(prompt.lower().split())
    answer_words = set(answer.lower().split())
    common = prompt_words.intersection(answer_words)
    return min(len(common) / (len(prompt_words) + 1), 0.5)

def final_score(prompt, answer):
    sem = semantic_score(answer, prompt)
    length = length_score(answer)
    keyword = keyword_score(prompt, answer)

    # Base weighted score
    base = (
        0.5 * sem +
        0.3 * length +
        0.2 * keyword
    )

    # 🔥 HARD PENALTIES
    if length < 0.2:
        base *= 0.4   # very short → crush score

    if sem < 0.3:
        base *= 0.5   # irrelevant → heavy penalty

    # 🔥 BOOST GOOD ANSWERS
    if sem > 0.75 and length > 0.6:
        base *= 1.2

    # 🔥 SCORE STRETCHING (KEY FIX)
    # expand mid-range into full 0–100
    stretched = (base - 0.2) / (0.9 - 0.2)
    stretched = max(0, min(stretched, 1))

    return round(stretched * 100, 2)