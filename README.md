# Market Intelligence & Competitor Analysis Platform

An AI-powered system that monitors competitor websites, detects meaningful changes, performs whitespace (market gap) analysis, generates ML-driven insights, analyzes sentiment, and presents everything through an interactive dashboard.
![Main Dashboard](assets/dashboard_main.png)
![Insights Dashboard](assets/dashboard_insights.png)
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

