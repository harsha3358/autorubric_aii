def keyword_overlap(prompt, answer):
    p = set(prompt.lower().split())
    a = set(answer.lower().split())

    if not p:
        return 0

    return len(p.intersection(a)) / len(p)


def length_score(answer):
    words = len(answer.split())

    if words > 120:
        return 1.0
    elif words > 80:
        return 0.85
    elif words > 50:
        return 0.7
    elif words > 25:
        return 0.5
    else:
        return 0.2


def structure_score(answer):
    sentences = [s for s in answer.split(".") if s.strip()]

    if len(sentences) >= 4:
        return 1.0
    elif len(sentences) >= 2:
        return 0.7
    else:
        return 0.3


def clarity_score(answer):
    words = answer.split()
    if not words:
        return 0.3

    avg_word_len = sum(len(w) for w in words) / len(words)

    if avg_word_len > 5:
        return 0.9
    elif avg_word_len > 4:
        return 0.7
    else:
        return 0.5


def evaluate_metrics(prompt, answer):
    k = keyword_overlap(prompt, answer)
    l = length_score(answer)
    s = structure_score(answer)
    c = clarity_score(answer)

    return {
        "relevance": round(k * 100, 2),
        "depth": round(l * 100, 2),
        "structure": round(s * 100, 2),
        "clarity": round(c * 100, 2),
    }


def final_score(metrics):
    base = (
        0.35 * (metrics["relevance"] / 100) +
        0.30 * (metrics["depth"] / 100) +
        0.20 * (metrics["structure"] / 100) +
        0.15 * (metrics["clarity"] / 100)
    )

    return round(base * 100, 2)