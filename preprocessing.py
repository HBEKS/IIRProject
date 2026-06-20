# Import modul-modul yang diperlukan
import re  # Untuk operasi regular expression
from langdetect import detect  # Untuk mendeteksi bahasa teks
from nltk.corpus import stopwords  # Untuk stopwords bahasa Inggris
from nltk.stem import PorterStemmer  # Untuk stemming bahasa Inggris
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory  # Untuk stemming bahasa Indonesia

# Inisialisasi stopwords dan stemmer untuk bahasa Inggris
stopwords_en = set(stopwords.words('english'))  # Set stopwords bahasa Inggris
stemmer_en = PorterStemmer()  # Stemmer Porter untuk bahasa Inggris

# Inisialisasi stemmer untuk bahasa Indonesia menggunakan Sastrawi
factory = StemmerFactory()
stemmer_id = factory.create_stemmer()

# Stopwords Indonesia yang lebih lengkap (ditulis sebagai multi-line string)
stopwords_id = set("""
yang dan di ke dari pada untuk dengan atau ini itu
dalam pada adalah sebagai oleh karena maka sehingga
juga telah bisa dapat agar supaya yaitu yakni
adalah yaitu yakni tentang terhadap tanpa melalui
tentu saja sangat amat terlalu lebih kurang
hanya saja cuma sekadar bahwa bahwasannya
apabila jika jikalau ketika sewaktu demi untuk
sambil seraya setelah sesudah sebelum sehabis
demi atas tentang menurut meskipun walaupun
sungguhpun biarpun kendatipun agar supaya seandainya
seakan seolah olah andaikata seumpama tentang
mengenai hal itu ini tersebut itu tersebutnya
adanya adanya pun per tersebutnya tadi
lagi pula makin kamu kami kita mereka ini itu
sini situ sana segala seluruh semua setiap
sebuah suatu beberapa berbagai macam
""".split())  # Split string menjadi list kata, lalu ubah ke set

# Kamus sinonim yang diperluas untuk query expansion
SYNONYMS = {
    # English keywords
    'optimization': ['optim', 'optimal', 'optimum', 'optimize', 'optimizing', 'optimisasi'],
    'network': ['net', 'networking', 'jaringan'],
    'security': ['secure', 'safety', 'keamanan', 'protection'],
    'analysis': ['analisa', 'analisis', 'analyze'],
    'data': ['datum', 'information', 'informasi'],
    'system': ['sistem', 'systems'],
    'model': ['modeling', 'modelling', 'pemodelan'],
    'algorithm': ['algoritma', 'algoritme'],
    'performance': ['kinerja', 'performa'],
    'design': ['desain', 'rancangan'],
    
    # Indonesia keywords
    'optimisasi': ['optimization', 'optim', 'optimal', 'pengoptimalan'],
    'jaringan': ['network', 'net', 'networking'],
    'keamanan': ['security', 'secure', 'safety'],
    'analisis': ['analysis', 'analisa', 'analyze'],
    'sistem': ['system', 'systems'],
    'model': ['modeling', 'modelling', 'pemodelan'],
    'algoritma': ['algorithm', 'algoritme'],
    'kinerja': ['performance', 'performa'],
    'desain': ['design', 'rancangan'],
}

def clean_text(text):
    """Membersihkan teks dari karakter tidak penting"""
    text = text.lower()  # Ubah ke lowercase
    text = re.sub(r"[^a-zA-Z\s]", " ", text)  # Hapus karakter non-alfabet (hanya simpan huruf dan spasi)
    text = re.sub(r"\s+", " ", text).strip()  # Normalisasi spasi (ubah multiple space jadi single space)
    return text

def tokenize(text):
    """Memecah teks menjadi token (kata-kata individual)"""
    return text.split()  # Split berdasarkan spasi

def preprocess_english(text):
    """Preprocessing untuk teks bahasa Inggris"""
    text = clean_text(text)  # Bersihkan teks
    tokens = tokenize(text)  # Tokenisasi
    tokens = [t for t in tokens if t not in stopwords_en]  # Hapus stopwords
    tokens = [stemmer_en.stem(t) for t in tokens]  # Stemming menggunakan Porter Stemmer
    return tokens

def preprocess_indonesia(text):
    """Preprocessing untuk teks bahasa Indonesia"""
    text = clean_text(text)  # Bersihkan teks
    tokens = tokenize(text)  # Tokenisasi
    tokens = [t for t in tokens if t not in stopwords_id]  # Hapus stopwords Indonesia
    if tokens:
        text = " ".join(tokens)  # Gabungkan token menjadi string
        text = stemmer_id.stem(text)  # Stemming menggunakan Sastrawi
        return text.split()  # Kembalikan sebagai list token
    return []  # Return list kosong jika tidak ada token

def preprocess_title(title):
    """Preprocessing utama untuk judul artikel"""
    try:
        lang = detect(title)  # Deteksi bahasa judul
    except:
        lang = "unknown"  # Default jika deteksi gagal

    # Proses berdasarkan bahasa yang terdeteksi
    if lang == "id":  # Jika bahasa Indonesia
        tokens = preprocess_indonesia(title)
        language = "Indonesian"
    else:  # Default ke bahasa Inggris
        tokens = preprocess_english(title)
        language = "English"

    return {
        "original": title,  # Judul asli
        "language": language,  # Bahasa yang terdeteksi
        "tokens": tokens  # Token hasil preprocessing
    }

def preprocess_for_query(keyword):
    """
    Preprocessing khusus untuk keyword/query pencarian
    Deteksi bahasa secara otomatis dan gunakan preprocessing yang sesuai
    """
    
    # Validasi input keyword
    if not keyword or not keyword.strip():
        return []  # Return list kosong jika keyword kosong
    
    # Deteksi bahasa keyword
    try:
        lang = detect(keyword)
    except:
        lang = "en"  # Default ke English jika deteksi gagal
    
    # Bersihkan teks keyword
    text = clean_text(keyword)
    
    # Validasi setelah cleaning
    if not text:
        return []  # Return list kosong jika tidak ada teks setelah cleaning
    
    # Tokenisasi
    tokens = tokenize(text)
    
    # Preprocessing berdasarkan bahasa
    if lang == "id":  # Bahasa Indonesia
        filtered_tokens = [t for t in tokens if t not in stopwords_id]  # Hapus stopwords
        if filtered_tokens:
            text_to_stem = " ".join(filtered_tokens)  # Gabungkan untuk stemming
            stemmed_text = stemmer_id.stem(text_to_stem)  # Stemming
            result_tokens = stemmed_text.split()  # Kembalikan ke list token
        else:
            result_tokens = []  # List kosong jika semua token stopwords
    else:  # Bahasa Inggris atau lainnya
        filtered_tokens = [t for t in tokens if t not in stopwords_en]  # Hapus stopwords
        result_tokens = [stemmer_en.stem(t) for t in filtered_tokens]  # Stemming
    
    # Filter token pendek (kurang dari 2 karakter)
    result_tokens = [t for t in result_tokens if t and len(t) > 1]
    
    # Fallback: jika semua token terfilter, ambil token yang lebih panjang
    if not result_tokens:
        if lang == "id":
            filtered_tokens = [t for t in tokens if t not in stopwords_id and len(t) > 2]
        else:
            filtered_tokens = [t for t in tokens if t not in stopwords_en and len(t) > 2]
        
        if filtered_tokens:
            result_tokens = filtered_tokens  # Gunakan token dengan filter longgar
        else:
            # Fallback terakhir: ambil semua token dengan panjang > 2
            result_tokens = [t for t in tokens if len(t) > 2]
    
    # Tambahkan sinonim ke query (query expansion)
    expanded_tokens = add_synonyms_to_query(result_tokens)
    
    # Hapus duplikat dengan menjaga urutan
    final_tokens = []
    seen = set()  # Set untuk tracking token yang sudah ada
    for token in expanded_tokens:
        if token not in seen:
            seen.add(token)  # Tambahkan ke set
            final_tokens.append(token)  # Tambahkan ke list final
    
    return final_tokens

def add_synonyms_to_query(tokens):
    """Menambahkan sinonim ke dalam query untuk meningkatkan recall"""
    expanded = list(tokens)  # Copy list token asli
    
    # Untuk setiap token, cek apakah ada di kamus sinonim
    for token in tokens:
        if token in SYNONYMS:
            # Tambahkan semua sinonim ke list
            for synonym in SYNONYMS[token]:
                if synonym not in expanded:  # Hindari duplikat
                    expanded.append(synonym)
    
    return expanded