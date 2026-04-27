import numpy as np

def simple_similarity(a, b):
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())

    if not a_words:
        return 0

    return len(a_words.intersection(b_words)) / len(a_words)

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

def final_score(prompt, answer):
    sim = simple_similarity(prompt, answer)
    length = length_score(answer)

    score = (0.6 * sim + 0.4 * length)

    if length < 0.2:
        score *= 0.5

    return round(score * 100, 2)