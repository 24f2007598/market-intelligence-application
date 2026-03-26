import os

# POSTGRES_URI = "postgresql://user:password@localhost:5432/market_db"
POSTGRES_URI = "postgresql:///market_db"

DB_CONFIG = {
    "dbname": "market_db",
    "host": "localhost"
}

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

COLLECTION_NAME = "market_intel"