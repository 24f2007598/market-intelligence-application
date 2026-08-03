"""
db/db.py — Database layer.

Uses SQLAlchemy so it works with both:
  - SQLite  (default / Streamlit Cloud)
  - PostgreSQL (local dev / production)

The DATABASE_URL env var controls which backend is used.
"""
from sqlalchemy import create_engine, text
from utils.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    # SQLite needs this; ignored by Postgres
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)


def _init_sqlite_tables():
    """Create tables if using SQLite and they don't exist yet."""
    if not DATABASE_URL.startswith("sqlite"):
        return
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS competitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competitor_id INTEGER,
                url TEXT,
                page_type TEXT,
                snapshot_date TEXT
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id INTEGER,
                raw_text TEXT,
                cleaned_text TEXT
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                company TEXT,
                product TEXT,
                review_text TEXT,
                rating REAL,
                sentiment_label TEXT,
                sentiment_score REAL,
                sentiment_updated_at TEXT,
                timestamp TEXT
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                snapshot_date TEXT,
                old_text TEXT,
                new_text TEXT,
                change_type TEXT,
                change_confidence REAL,
                timestamp TEXT,
                source TEXT
            )
        """))
        conn.commit()


# Auto-initialise SQLite tables on import
_init_sqlite_tables()


# ─── Competitor ───────────────────────────────────────────────
def insert_competitor(name):
    with engine.connect() as conn:
        res = conn.execute(
            text("INSERT INTO competitors (name) VALUES (:name)"),
            {"name": name}
        )
        conn.commit()
        return res.lastrowid


# ─── Pages ────────────────────────────────────────────────────
def insert_page(cid, url, ptype, snapshot):
    with engine.connect() as conn:
        res = conn.execute(
            text("""
                INSERT INTO pages (competitor_id, url, page_type, snapshot_date)
                VALUES (:cid, :url, :ptype, :snap)
            """),
            {"cid": cid, "url": url, "ptype": ptype, "snap": snapshot}
        )
        conn.commit()
        return res.lastrowid


# ─── Documents ────────────────────────────────────────────────
def insert_document(pid, raw, clean):
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO documents (page_id, raw_text, cleaned_text)
                VALUES (:pid, :raw, :clean)
            """),
            {"pid": pid, "raw": raw, "clean": clean}
        )
        conn.commit()


# ─── Reviews ──────────────────────────────────────────────────
def insert_review(source, company, review_text):
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO reviews (source, company, review_text)
                VALUES (:s, :c, :r)
            """),
            {"s": source, "c": company, "r": review_text}
        )
        conn.commit()


def insert_reviews(reviews):
    """Bulk insert reviews (from synthetic data scripts)."""
    with engine.connect() as conn:
        for r in reviews:
            conn.execute(
                text("""
                    INSERT INTO reviews (id, product, review_text, rating, sentiment_label, timestamp, source)
                    VALUES (:id, :product, :review_text, :rating, :sentiment_label, :timestamp, :source)
                """),
                {
                    "id": r.get("id"),
                    "product": r.get("product"),
                    "review_text": r.get("review_text"),
                    "rating": r.get("rating"),
                    "sentiment_label": r.get("sentiment_label"),
                    "timestamp": r.get("timestamp"),
                    "source": "synthetic"
                }
            )
        conn.commit()


def get_unlabeled_reviews(limit=500):
    with engine.connect() as conn:
        res = conn.execute(
            text("""
                SELECT id, review_text
                FROM reviews
                WHERE review_text IS NOT NULL AND sentiment_label IS NULL
                LIMIT :limit
            """),
            {"limit": limit}
        ).fetchall()
        return [{"id": r[0], "text": r[1]} for r in res]


def update_review_sentiment(review_id, label, score):
    from datetime import datetime
    with engine.connect() as conn:
        conn.execute(
            text("""
                UPDATE reviews
                SET sentiment_label = :label,
                    sentiment_score = :score,
                    sentiment_updated_at = :updated_at
                WHERE id = :id
            """),
            {"label": label, "score": score, "updated_at": str(datetime.now()), "id": review_id}
        )
        conn.commit()


# ─── Changes ──────────────────────────────────────────────────
def insert_change(url, snapshot_date, old_text, new_text, change_type, confidence):
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO changes (url, snapshot_date, old_text, new_text, change_type, change_confidence)
                VALUES (:url, :snap, :old, :new, :type, :conf)
            """),
            {"url": url, "snap": snapshot_date, "old": old_text, "new": new_text,
             "type": change_type, "conf": confidence}
        )
        conn.commit()


def insert_changes(changes):
    """Bulk insert changes (from synthetic data scripts)."""
    with engine.connect() as conn:
        for c in changes:
            conn.execute(
                text("""
                    INSERT INTO changes (url, old_text, new_text, change_type, timestamp, source)
                    VALUES (:url, :old_text, :new_text, :change_type, :timestamp, :source)
                """),
                {
                    "url": c.get("url"),
                    "old_text": c.get("old_text"),
                    "new_text": c.get("new_text"),
                    "change_type": c.get("change_type"),
                    "timestamp": c.get("timestamp"),
                    "source": "synthetic"
                }
            )
        conn.commit()