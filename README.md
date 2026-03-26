# Market Intelligence & Competitor Analysis Platform

An AI-powered system that monitors competitor websites, detects meaningful changes, performs whitespace (market gap) analysis, generates ML-driven insights, analyzes sentiment, and presents everything through an interactive dashboard.

<img width="536" height="332" alt="image" src="https://github.com/user-attachments/assets/76f8a191-bfa6-49d4-80a3-63eaadc0597e" />
<img width="637" height="299" alt="image" src="https://github.com/user-attachments/assets/c04b5154-9c19-41e4-854a-9e6009ae4ba8" />



---

## Overview

This project transforms raw competitor data into actionable insights by combining:

- Website monitoring  
- Whitespace (gap) detection  
- Machine learning insights  
- Sentiment analysis  
- RAG-based explanations  
- Interactive dashboard visualization  

---

## Core Features

### Website Monitoring & Snapshot Tracking
- Periodic scraping of competitor websites  
- Stores timestamped snapshots  
- Enables historical comparison  

---

### 🧹 Data Cleaning & Normalization
- Removes HTML, scripts, and noise  
- Standardizes formatting  
- Prepares data for ML + RAG  

---

### 🔄 Change Detection
Detects meaningful changes like:
- Pricing updates  
- Feature additions/removals  
- Messaging changes  

Ignores:
- Whitespace changes  
- Minor formatting differences  

---

### Whitespace Analysis (Market Gap Detection)
- Identifies what competitors are NOT doing  
- Detects:
  - Missing features  
  - Untapped opportunities  
  - Industry gaps  
- Helps businesses find competitive advantage  

---

### ML-Based Insights
- Applies machine learning to extracted data  
- Identifies patterns across competitors  
- Generates:
  - Strategic insights  
  - Feature importance  
  - Trend signals  

---

### Sentiment Analysis Model
- Analyzes reviews / textual content  
- Classifies sentiment:
  - Positive  
  - Negative  
  - Neutral  
- Helps understand competitor perception  

---

### RAG Pipeline (Natural Language Insights)
- Retrieves relevant data from vector DB  
- Generates human-readable explanations  

Example:
> “What are competitors missing in their product?”  
→ Returns gap analysis in simple language  

---

### Interactive Dashboard
- Built using Streamlit  
- Displays:
  - Competitor insights  
  - Sentiment distribution  
  - Detected changes  
  - Market gaps  
- Provides a user-friendly interface for decision-making  

---

## 🏗️ Architecture
Data Ingestion (Scraping / Wayback)
↓
Cleaning & Normalization
↓
Chunking
↓
Embedding Generation
↓
Vector Storage (Qdrant)
↓
Change Detection
↓
ML + Sentiment Analysis
↓
RAG Pipeline
↓
Natural Language Output


---

## ⚙️ Tech Stack

### AI / ML
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Custom ML models  
- Sentiment analysis  

### Backend
- Python  
- FastAPI  

### RAG & Embeddings
- Qdrant (vector database)  
- HuggingFace embeddings  

### Data Collection
- Playwright  
- Wayback Machine  

### Storage
- JSON / database (snapshots)  
- Qdrant (vector storage)  

### Frontend
- Streamlit  

### DevOps
- Docker  

---

## 🛠️ Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-repo/market-intelligence.git
cd market-intelligence
