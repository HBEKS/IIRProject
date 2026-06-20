import math  # Untuk fungsi logaritma
from collections import Counter  # Untuk menghitung frekuensi term

def compute_tf(doc):
    """
    Menghitung Term Frequency (TF) untuk sebuah dokumen.
    TF = frekuensi term di dokumen / total term di dokumen.
    """
    if not doc:  # Jika dokumen kosong
        return {}  # Return dictionary kosong
    
    tf = {}  # Dictionary untuk menyimpan TF
    count = Counter(doc)  # Hitung frekuensi setiap term dalam dokumen
    total_terms = len(doc)  # Total jumlah term dalam dokumen

    # Hitung TF untuk setiap term
    for term, freq in count.items():
        tf[term] = freq / total_terms  # TF = frekuensi term / total term

    return tf  # Return dictionary TF

def compute_df(docs):
    """
    Menghitung Document Frequency (DF) untuk kumpulan dokumen.
    DF = jumlah dokumen yang mengandung suatu term.
    """
    df = {}  # Dictionary untuk menyimpan DF

    for doc in docs:  # Loop melalui setiap dokumen
        if not doc:  # Skip jika dokumen kosong
            continue
        unique_terms = set(doc)  # Ambil term unik dalam dokumen
        for term in unique_terms:  # Untuk setiap term unik
            # Increment counter untuk term ini
            df[term] = df.get(term, 0) + 1

    return df  # Return dictionary DF

def compute_idf(df, total_docs):
    """
    Menghitung Inverse Document Frequency (IDF) dengan smoothing.
    IDF = log((N + 1) / (DF + 1)) + 1
    Smoothing (+1) mencegah division by zero dan infinite IDF.
    """
    idf = {}  # Dictionary untuk menyimpan IDF

    for term, freq in df.items():  # Loop melalui setiap term
        # Hitung IDF dengan smoothing
        # log((total dokumen + 1) / (DF term + 1)) + 1
        idf[term] = math.log((total_docs + 1) / (freq + 1)) + 1

    return idf  # Return dictionary IDF

def compute_tfidf(tf, idf):
    """
    Menghitung TF-IDF untuk dokumen atau query.
    TF-IDF = TF * IDF
    """
    tfidf = {}  # Dictionary untuk menyimpan TF-IDF

    for term, tf_val in tf.items():  # Loop melalui setiap term dalam TF
        # Ambil nilai IDF untuk term ini, default 0 jika tidak ada
        idf_val = idf.get(term, 0)
        # Hitung TF-IDF
        tfidf[term] = tf_val * idf_val

    return tfidf  # Return dictionary TF-IDF

def build_tfidf_vectors(documents, query_tokens):
    """
    Membangun vektor TF-IDF untuk semua dokumen dan query.
    Mengembalikan:
    - doc_vectors: list of dictionaries (TF-IDF untuk setiap dokumen)
    - query_vector: dictionary (TF-IDF untuk query)
    """
    
    # Filter dokumen yang tidak kosong
    valid_docs = [doc for doc in documents if doc]
    
    if not valid_docs:  # Jika tidak ada dokumen valid
        return [], {}  # Return list dan dictionary kosong
    
    # Hitung TF untuk setiap dokumen valid
    tfs = [compute_tf(doc) for doc in valid_docs]
    
    # Hitung DF untuk semua dokumen
    df = compute_df(valid_docs)
    # Hitung IDF berdasarkan DF dan jumlah dokumen
    idf = compute_idf(df, len(valid_docs))
    
    # Hitung TF-IDF untuk setiap dokumen
    doc_vectors = [compute_tfidf(tf, idf) for tf in tfs]
    
    # Hitung TF-IDF untuk query
    query_tf = compute_tf(query_tokens)  # TF untuk query
    query_vector = compute_tfidf(query_tf, idf)  # TF-IDF untuk query
    
    return doc_vectors, query_vector  # Return vektor dokumen dan query