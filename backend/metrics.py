import string
import re

STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def get_keywords(text):
    words = clean_text(text).split()
    return set([w for w in words if w not in STOP_WORDS])

def keyword_overlap(prompt, answer):
    p_keys = get_keywords(prompt)
    a_keys = get_keywords(answer)

    if not p_keys:
        return 0

    return len(p_keys.intersection(a_keys)) / len(p_keys)

def length_score(answer):
    words = len(clean_text(answer).split())

    if words > 100:
        return 1.0
    elif words > 60:
        return 0.85
    elif words > 30:
        return 0.7
    elif words > 15:
        return 0.5
    else:
        return 0.2

def structure_score(answer):
    # Split by actual sentence terminators
    sentences = [s for s in re.split(r'[.!?]+', answer) if s.strip()]

    if len(sentences) >= 5:
        return 1.0
    elif len(sentences) >= 3:
        return 0.8
    elif len(sentences) >= 2:
        return 0.6
    else:
        return 0.3

def clarity_score(answer):
    words = clean_text(answer).split()
    if not words:
        return 0.3

    # Avoid penalizing if words are just normal length
    avg = sum(len(w) for w in words) / len(words)

    if avg >= 4.5:
        return 1.0
    elif avg >= 4.0:
        return 0.8
    elif avg >= 3.5:
        return 0.6
    else:
        return 0.4

def evaluate_metrics(prompt, answer):
    return {
        "relevance": round(keyword_overlap(prompt, answer) * 100, 2),
        "depth": round(length_score(answer) * 100, 2),
        "structure": round(structure_score(answer) * 100, 2),
        "clarity": round(clarity_score(answer) * 100, 2),
    }

def final_score(metrics):
    base = (
        0.40 * (metrics["relevance"] / 100) +
        0.25 * (metrics["depth"] / 100) +
        0.20 * (metrics["structure"] / 100) +
        0.15 * (metrics["clarity"] / 100)
    )

    return round(base * 100, 2)