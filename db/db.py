from sqlalchemy import create_engine, text
from utils.config import POSTGRES_URI

engine = create_engine(POSTGRES_URI)


def insert_competitor(name):
    with engine.connect() as conn:
        res = conn.execute(
            text("INSERT INTO competitors (name) VALUES (:name) RETURNING id"),
            {"name": name}
        )
        conn.commit()
        return res.fetchone()[0]


def insert_page(cid, url, ptype, snapshot):
    with engine.connect() as conn:
        res = conn.execute(
            text("""
                INSERT INTO pages (competitor_id, url, page_type, snapshot_date)
                VALUES (:cid, :url, :ptype, :snap)
                RETURNING id
            """),
            {"cid": cid, "url": url, "ptype": ptype, "snap": snapshot}
        )
        conn.commit()
        return res.fetchone()[0]


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
            {"label": label, "score": score, "updated_at": datetime.now(), "id": review_id}
        )
        conn.commit()


def insert_change(url, snapshot_date, old_text, new_text, change_type, confidence):
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO changes (url, snapshot_date, old_text, new_text, change_type, change_confidence)
                VALUES (:url, :snap, :old, :new, :type, :conf)
            """),
            {"url": url, "snap": snapshot_date, "old": old_text, "new": new_text, "type": change_type, "conf": confidence}
        )
        conn.commit()


# from sqlalchemy import create_engine, text
# from utils.config import POSTGRES_URI

# engine = create_engine(POSTGRES_URI)

# def insert_competitor(name):
#     with engine.connect() as conn:
#         res = conn.execute(
#             text("INSERT INTO competitors (name) VALUES (:name) RETURNING id"),
#             {"name": name}
#         )
#         conn.commit()
#         return res.fetchone()[0]


# def insert_page(competitor_id, url, page_type, snapshot):
#     with engine.connect() as conn:
#         res = conn.execute(
#             text("""
#                 INSERT INTO pages (competitor_id, url, page_type, snapshot_date)
#                 VALUES (:cid, :url, :ptype, :snap)
#                 RETURNING id
#             """),
#             {"cid": competitor_id, "url": url, "ptype": page_type, "snap": snapshot}
#         )
#         conn.commit()
#         return res.fetchone()[0]


# def insert_document(page_id, raw_text, cleaned_text):
#     with engine.connect() as conn:
#         conn.execute(
#             text("""
#                 INSERT INTO documents (page_id, raw_text, cleaned_text)
#                 VALUES (:pid, :raw, :clean)
#             """),
#             {"pid": page_id, "raw": raw_text, "clean": cleaned_text}
#         )
#         conn.commit()


# def insert_review(source, company, review_text):
#     with engine.connect() as conn:
#         conn.execute(
#             text("""
#                 INSERT INTO reviews (source, company, review_text)
#                 VALUES (:s, :c, :r)
#             """),
#             {"s": source, "c": company, "r": review_text}
#         )
#         conn.commit()