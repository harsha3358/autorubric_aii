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
    sentences = answer.split(".")
    if len(sentences) >= 4:
        return 1.0
    elif len(sentences) >= 2:
        return 0.7
    else:
        return 0.3


def final_score(prompt, answer):
    k = keyword_overlap(prompt, answer)
    l = length_score(answer)
    s = structure_score(answer)

    # weighted scoring
    base = (0.4 * k) + (0.35 * l) + (0.25 * s)

    # penalties
    if l < 0.3:
        base *= 0.6

    # boost good answers
    if k > 0.6 and l > 0.7:
        base *= 1.2

    # normalize to full range
    score = max(0, min(base, 1))

    return round(score * 100, 2)