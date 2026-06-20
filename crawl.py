# Import modul-modul yang diperlukan
import requests, sys, json, time, re, io
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from preprocessing import preprocess_title, preprocess_for_query
from tfidf import build_tfidf_vectors
from similarity import cosine_similarity

# FIX: Set encoding UTF-8 untuk stdout dan stderr agar support karakter non-ASCII
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Base URL untuk Google Scholar
BASE = "https://scholar.google.com"

# Ambil parameter dari command line
author  = sys.argv[1]   # Nama author pertama
keyword = sys.argv[2].lower()  # Kata kunci pencarian (diubah ke lowercase)
limit   = int(sys.argv[3])  # Jumlah maksimal artikel yang diambil

# Headers untuk request HTTP (simulasi browser)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",  # Preferensi bahasa
    "Referer": "https://scholar.google.com/"  # Referer header
}

# Buat session untuk maintain cookies dan headers
session = requests.Session()
session.headers.update(headers)

def get_author_id(author_name):
    """Mencari Author ID dari Google Scholar berdasarkan nama author"""
    # Bangun URL pencarian author
    search_url = (
        f"{BASE}/citations?"
        f"hl=en&view_op=search_authors&mauthors={author_name.replace(' ', '+')}"
    )

    # Lakukan request ke halaman pencarian author
    resp = session.get(search_url, timeout=30)
    soup = BeautifulSoup(resp.text, "html.parser")  # Parse HTML

    # Cari link author di halaman hasil pencarian
    link = soup.select_one("a.gs_ai_name")
    if link:
        href = link.get("href", "")
        m = re.search(r"user=([\w-]+)", href)  # Ekstrak user ID dari URL
        if m:
            return m.group(1)  # Return author ID jika ditemukan
        
    # Fallback: cari di halaman scholar biasa
    scholar_search = f"{BASE}/scholar?q={author_name.replace(' ', '+')}"
    resp = session.get(scholar_search, timeout=30)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Cari link citations di halaman scholar
    link = soup.select_one('a[href^="/citations?user="]')
    if not link:
        return None  # Return None jika tidak ditemukan

    href = link.get("href", "")
    m = re.search(r"user=([\w-]+)", href)  # Ekstrak user ID
    if m:
        return m.group(1)

    return None  # Return None jika tidak ditemukan

def normalize_date(date_str):
    """Normalisasi format tanggal dari berbagai format ke format Indonesia"""
    # Mapping bulan angka ke nama bulan Indonesia
    bulan = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }

    # Format: YYYY/MM/DD
    m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})", date_str)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{d} {bulan.get(mo, '')} {y}"  # Format: DD Bulan YYYY

    # Format: YYYY saja
    m = re.match(r"(\d{4})", date_str)
    if m:
        return f"1 Januari {m.group(1)}"  # Default ke 1 Januari

    return "-"  # Return dash jika format tidak dikenali

# PROFIL AUTHOR
# Cari ID author berdasarkan nama yang diberikan
AUTHOR_ID = get_author_id(author)

# Jika author tidak ditemukan, keluarkan error dan exit
if not AUTHOR_ID:
    print(json.dumps({
        "error": f"Author '{author}' tidak ditemukan di Google Scholar"
    }))
    sys.exit(0)  # Exit dengan kode 0

# Bangun URL profil author
profile_url = f"{BASE}/citations?user={AUTHOR_ID}&hl=en&pagesize=100"
resp = session.get(profile_url, timeout=30)
resp.raise_for_status()  # Raise exception jika request gagal

# Parse HTML halaman profil
soup = BeautifulSoup(resp.text, "html.parser")
rows = soup.select("tr.gsc_a_tr")  # Select semua baris artikel

results = []  # List untuk menyimpan hasil

# LOOP ARTIKEL - TANPA FILTERING KEYWORD (ambil semua dulu)
article_count = 0  # Counter artikel yang sudah diambil
for i, row in enumerate(rows):
    if article_count >= limit:  # Hentikan jika sudah mencapai limit
        break
        
    # Cari elemen judul artikel
    title_el = row.select_one("a.gsc_a_at")
    if not title_el:  # Skip jika tidak ada judul
        continue

    title = title_el.text.strip()  # Ambil teks judul
    
    # Dapatkan URL detail artikel
    view_url = urljoin(BASE, title_el["href"])

    time.sleep(2)  # Delay 2 detik untuk menghindari blocking oleh Google
    # Request halaman detail artikel
    art_resp = session.get(view_url, timeout=30)
    art_resp.raise_for_status()  # Raise exception jika request gagal
    
    art_soup = BeautifulSoup(art_resp.text, "html.parser")  # Parse HTML detail artikel

    # PREPROCESS TITLE untuk dokumen (tokenisasi, stopword removal, dll)
    processed = preprocess_title(title)

    # Struktur data untuk artikel
    data = {
        "judul": title,  # Judul asli
        "penulis": "-",  # Default value
        "tanggal": "-",  # Default value
        "jurnal": "-",  # Default value
        "sitasi": "-",  # Default value
        "link": "-",  # Default value
        "similarity": 0.0,  # Skor similarity awal
        "tokens": processed["tokens"],  # Token hasil preprocessing
        "language": processed["language"],  # Bahasa judul
        "raw_title": title.lower()  # Judul lowercase untuk matching
    }

    # EKSTRAK METADATA dari halaman detail
    fields = art_soup.select(".gsc_oci_field")  # Field metadata
    values = art_soup.select(".gsc_oci_value")  # Value metadata

    # Loop melalui field dan value yang tersedia
    for j in range(min(len(fields), len(values))):
        key = fields[j].text.strip().lower()  # Nama field (lowercase)
        val = values[j].text.strip()  # Value field

        # Mapping field ke struktur data
        if key == "authors":
            data["penulis"] = val  # Simpan penulis
        elif key == "publication date":
            data["tanggal"] = normalize_date(val)  # Normalisasi tanggal
        elif key in ["journal", "conference"]:
            data["jurnal"] = val  # Simpan nama jurnal/konferensi
        elif key == "publisher" and data["jurnal"] == "-":
            data["jurnal"] = val  # Gunakan publisher jika jurnal kosong
        elif key == "total citations":
            # Cari link "Cited by"
            a = values[j].find("a", string=lambda t: t and "Cited by" in t)
            if a:
                # Ekstrak angka citations dari teks
                m = re.search(r"Cited by\s+(\d+)", a.get_text(" ", strip=True))
                if m:
                    data["sitasi"] = m.group(1)  # Simpan jumlah sitasi
            else:
                # Fallback: cari di teks biasa
                m = re.search(r"Cited by\s+(\d+)", values[j].get_text(" ", strip=True))
                if m:
                    data["sitasi"] = m.group(1)

    # LINK JURNAL / PDF
    pdf_el = art_soup.select_one("div.gsc_oci_title_ggi a")
    if pdf_el and pdf_el.get("href"):
        url = pdf_el["href"]  # URL PDF/jurnal
        data["link"] = url
        host = urlparse(url).netloc  # Ekstrak hostname
        data["link_text"] = host if host else url  # Tampilkan hostname
    else:
        data["link"] = view_url  # Fallback ke URL scholar
        data["link_text"] = "scholar.google.com"

    results.append(data)  # Tambahkan artikel ke results
    article_count += 1  # Increment counter

# PREPROCESS KEYWORD (QUERY) untuk perhitungan similarity
query_tokens = preprocess_for_query(keyword)

# Hitung similarity dengan TF-IDF jika ada hasil dan keyword
if results and query_tokens:
    # Ambil token dari setiap dokumen
    documents = [item["tokens"] for item in results]
    
    # Bangun vektor TF-IDF
    try:
        doc_vectors, query_vector = build_tfidf_vectors(documents, query_tokens)
        
        # Hitung similarity untuk setiap artikel
        for i in range(len(results)):
            if doc_vectors[i] and query_vector:  # Pastikan vektor valid
                score = cosine_similarity(doc_vectors[i], query_vector)
                # Pastikan score antara 0 dan 1
                score = max(0.0, min(1.0, score))
                results[i]["similarity"] = round(score, 4)  # Simpan score
            else:
                results[i]["similarity"] = 0.0  # Default 0 jika error
    except Exception as e:
        # Jika TF-IDF error, gunakan similarity sederhana (Jaccard-like)
        for i, result in enumerate(results):
            doc_tokens = result["tokens"]
            doc_set = set(doc_tokens)  # Set token dokumen
            query_set = set(query_tokens)  # Set token query
            
            if query_tokens:
                # Hitung intersection token
                common_tokens = doc_set.intersection(query_set)
                # Similarity = persentase token query yang muncul di dokumen
                simple_similarity = len(common_tokens) / len(query_tokens)
                results[i]["similarity"] = round(simple_similarity, 4)
            else:
                results[i]["similarity"] = 0.0

# Tambahkan bonus untuk exact match di judul (untuk meningkatkan relevansi)
for i, result in enumerate(results):
    title = result["judul"]
    if keyword.lower() in title.lower():
        # Tambah bonus 0.3 untuk exact match (maksimal 1.0)
        results[i]["similarity"] = min(1.0, results[i]["similarity"] + 0.3)
        results[i]["contains_keyword"] = True  # Flag exact match
    else:
        results[i]["contains_keyword"] = False

# Sort hasil berdasarkan similarity (descending/tertinggi ke terendah)
results = sorted(results, key=lambda x: x["similarity"], reverse=True)

# Struktur output final
output_data = {
    "author_id": AUTHOR_ID,  # ID author Google Scholar
    "author": author,  # Nama author
    "keyword": keyword,  # Kata kunci pencarian
    "limit": limit,  # Limit yang diminta
    "total_found": len(results),  # Jumlah artikel yang ditemukan
    "results": results  # List hasil artikel
}

# Output hasil dalam format JSON (tanpa ASCII escaping untuk support Unicode)
print(json.dumps(output_data, ensure_ascii=False))