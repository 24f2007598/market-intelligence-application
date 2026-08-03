import os
from dotenv import load_dotenv

load_dotenv(override=True)

# ─── Database ─────────────────────────────────────────────────
# Reads DATABASE_URL from env. Falls back to SQLite for Streamlit Cloud.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./market_intel.db")

# Legacy aliases (used by db/db.py psycopg2 path — only relevant locally)
POSTGRES_URI = DATABASE_URL

DB_CONFIG = {
    "dbname": os.getenv("PGDATABASE", "market_db"),
    "host":   os.getenv("PGHOST", "localhost"),
    "user":   os.getenv("PGUSER", ""),
    "password": os.getenv("PGPASSWORD", ""),
}

# ─── Qdrant Vector DB ─────────────────────────────────────────
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_URL  = os.getenv("QDRANT_URL", "")        # Qdrant Cloud URL (optional)
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "") # Qdrant Cloud API key (optional)

# ─── App Settings ─────────────────────────────────────────────
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "market_intel")

# ─── Google Gemini ────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")