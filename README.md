# 🔍 Intelligent Information Retrieval System for Scientific Articles

An **Intelligent Information Retrieval (IIR)** application that retrieves scientific publications from **Google Scholar** and ranks them using **Natural Language Processing (NLP)**, **TF-IDF**, and **Cosine Similarity**.

The system automatically detects document language (**English or Indonesian**), performs text preprocessing and query expansion, and returns the most relevant scientific articles based on user queries.

> 🎓 **University Project**
> 📅 **Development Period:** November 2025 – January 2026
> 👥 **Developed by a team of four Computer Science students**
> ✅ **Status:** Completed

---

## 🎯 Project Highlights

* Built an Information Retrieval system for scientific publications
* Applied **TF-IDF** and **Cosine Similarity** for document ranking
* Implemented bilingual NLP preprocessing (**English & Indonesian**)
* Performed Google Scholar web scraping to retrieve publication metadata
* Improved search relevance using query expansion techniques

---

## ✨ Features

* 🔎 Search scientific articles by **author name**
* 📝 Search publications using **custom keywords**
* 🌏 Automatic language detection (**English & Indonesian**)
* 🔄 Query expansion using synonym mapping
* 🧹 Natural Language Processing

  * Case Folding
  * Tokenization
  * Stopword Removal
  * Porter Stemmer
  * Sastrawi Stemmer
* 📊 TF-IDF document weighting
* 📈 Cosine Similarity ranking
* 📚 Display article metadata

  * Title
  * Authors
  * Journal
  * Publication Date
  * Citation Count
* 🔗 Direct access to journal pages
* 📉 Rank articles based on similarity score

---

## 🏗️ System Architecture

```text
Author + Keyword + Limit
            │
            ▼
Google Scholar Scraping
            │
            ▼
NLP Preprocessing
(Language Detection
Cleaning
Tokenization
Stopword Removal
Stemming
Query Expansion)
            │
            ▼
TF-IDF Vectorization
            │
            ▼
Cosine Similarity
            │
            ▼
Article Ranking
            │
            ▼
Display Results
```

---

## 🚀 Workflow

```text
👤 User
      →
🕷️ Google Scholar Scraping
      →
🧹 NLP Preprocessing
      →
🔄 Query Expansion
      →
📊 TF-IDF Vectorization
      →
📈 Cosine Similarity
      →
🏆 Ranking
      →
📚 Search Results
```

---

## ⚙️ Technologies Used

| Technology        | Purpose                      |
| ----------------- | ---------------------------- |
| Python            | Information Retrieval Engine |
| PHP               | Backend Integration          |
| HTML/CSS          | Frontend Interface           |
| XAMPP             | Apache Server                |
| Requests          | HTTP Client                  |
| BeautifulSoup     | Web Scraping                 |
| NLTK              | English NLP                  |
| Sastrawi          | Indonesian NLP               |
| LangDetect        | Language Detection           |
| TF-IDF            | Feature Weighting            |
| Cosine Similarity | Similarity Measurement       |

---

## 📂 Project Structure

```text
IIRProject/
│
├── index.html
├── result.php
├── crawl.py
├── preprocessing.py
├── tf-idf.py
├── similarity.py
├── requirements.txt
├── images/
│   ├── search-page.png
│   └── result-page.png
└── README.md
```

---

## ⚡ How It Works

1. The user enters an **author name**, **keyword**, and the **number of articles** to retrieve.

2. The system scrapes publication data from **Google Scholar**.

3. Retrieved article titles undergo NLP preprocessing:

   * Language Detection
   * Text Cleaning
   * Tokenization
   * Stopword Removal
   * Stemming

4. Query expansion enriches the user's query using predefined synonym mappings.

5. TF-IDF vectors are generated for both the query and article titles.

6. Cosine Similarity calculates the similarity score between the query and each article.

7. Articles are ranked from the highest similarity score to the lowest and displayed to the user.

---

## 📊 Similarity Formula

Cosine Similarity is computed as:

```text
              A · B
Similarity = ---------
            ||A|| ||B||
```

Where:

* **A** = Query vector
* **B** = Document vector

A score closer to **1** indicates higher relevance.

---

## 📷 Screenshots

### Search Page

```markdown
![Search Page](images/search-page.png)
```

### Search Results

```markdown
![Result Page](images/result-page.png)
```

> Replace the images above with screenshots from your application.

---

## 📦 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/IIRProject.git

cd IIRProject
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Place Project

Move the project into:

```text
xampp/
└── htdocs/
    └── IIRProject/
```

### Run Application

Start **Apache** using XAMPP and open:

```text
http://localhost/IIRProject/index.html
```

---

## 📋 Requirements

```text
langdetect
nltk
Sastrawi
requests
beautifulsoup4
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🎓 Academic Concepts Implemented

* Information Retrieval
* Natural Language Processing
* Web Scraping
* Language Detection
* Query Expansion
* TF-IDF
* Cosine Similarity
* Text Mining
* Ranking Algorithms

---

## 🚀 Future Improvements

Potential enhancements include:

* Implement semantic search using transformer embeddings
* Replace TF-IDF with dense vector embeddings
* Store article metadata in a database
* Add advanced filtering and sorting
* Integrate Retrieval-Augmented Generation (RAG)
* Export search results to PDF or CSV
* Build a REST API
* Deploy the application to a cloud platform

---

## 👥 Team Members

This project was collaboratively developed by:

* **Emanuel Jordan Rafhaelino Sanjaya**
* **Enrique Juan**
* **Tio Nauli Nadya Hutagalung**
* **Daniel Wuliutomo**

---

## ⭐ Acknowledgements

This project was developed as part of a university coursework to demonstrate the implementation of **Information Retrieval**, **Natural Language Processing**, and **Web Scraping** techniques for scientific article retrieval.

It showcases how **TF-IDF**, **Cosine Similarity**, and **NLP preprocessing** can be combined to improve the relevance of scientific literature retrieval from Google Scholar.
