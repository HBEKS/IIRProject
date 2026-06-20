import math

def cosine_similarity(vec1, vec2):
    """
    Menghitung cosine similarity antara dua vektor TF-IDF
    vec1, vec2: dict {term: tfidf_value}
    """
    if not vec1 or not vec2:
        return 0.0

    # ambil semua term unik
    terms = set(vec1.keys()) | set(vec2.keys())
    
    if not terms:
        return 0.0

    # dot product
    dot_product = 0.0
    for term in terms:
        dot_product += vec1.get(term, 0) * vec2.get(term, 0)

    # magnitude vektor 1
    mag1 = 0.0
    for term in terms:
        mag1 += vec1.get(term, 0) ** 2
    mag1 = math.sqrt(mag1)

    # magnitude vektor 2
    mag2 = 0.0
    for term in terms:
        mag2 += vec2.get(term, 0) ** 2
    mag2 = math.sqrt(mag2)

    if mag1 == 0 or mag2 == 0:
        return 0.0

    similarity = dot_product / (mag1 * mag2)
    
    # Pastikan similarity antara 0 dan 1
    return max(0.0, min(1.0, similarity))