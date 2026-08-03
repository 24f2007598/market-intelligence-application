"""
scripts/rag.py — RAG pipeline using Qdrant + Gemini.

On Streamlit Cloud, Qdrant is not available locally.
The code gracefully falls back to DB-only context if Qdrant is unreachable.
"""
import os
from dotenv import load_dotenv

load_dotenv(override=True)

from google import genai
from utils.config import (
    COLLECTION_NAME, GEMINI_API_KEY,
    QDRANT_HOST, QDRANT_PORT, QDRANT_URL, QDRANT_API_KEY
)
from db.db import engine
from sqlalchemy import text

# ─── Gemini client ────────────────────────────────────────────
client_gemini = genai.Client(api_key=GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"))

# ─── Qdrant client (optional — fails gracefully) ──────────────
_qdrant_available = False
client = None
embed_model = None

try:
    from qdrant_client import QdrantClient
    from sentence_transformers import SentenceTransformer

    if QDRANT_URL:
        # Qdrant Cloud
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY or None)
    else:
        # Local Qdrant
        client = QdrantClient(QDRANT_HOST, port=QDRANT_PORT)

    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    _qdrant_available = True
except Exception:
    _qdrant_available = False


def retrieve_context(query, k=5, change_filter=None):
    """Retrieve context from Qdrant (if available) + SQLite/Postgres DB."""
    qdrant_context = ""

    if _qdrant_available and client is not None:
        try:
            vector = embed_model.encode(query).tolist()

            query_filter = None
            if change_filter:
                from qdrant_client.http.models import Filter, FieldCondition, MatchValue
                query_filter = Filter(
                    must=[
                        FieldCondition(
                            key="change_type",
                            match=MatchValue(value=change_filter)
                        )
                    ]
                )

            results = client.query_points(
                collection_name=COLLECTION_NAME,
                query=vector,
                query_filter=query_filter,
                limit=k
            )
            hits = results.points if hasattr(results, "points") else results
            qdrant_context = "\n\n".join([h.payload["text"] for h in hits])
        except Exception:
            qdrant_context = ""

    # Always pull latest docs from SQL DB
    postgres_context = ""
    try:
        with engine.connect() as conn:
            rows = conn.execute(
                text("SELECT cleaned_text FROM documents ORDER BY id DESC LIMIT 3")
            ).fetchall()
        postgres_context = "\n\n".join([r[0] for r in rows if r[0]])
    except Exception:
        postgres_context = ""

    return (qdrant_context + "\n\n" + postgres_context).strip()


def generate_answer(query: str, change_filter=None):
    context = retrieve_context(query, change_filter=change_filter)

    system_insight = ""
    if change_filter:
        system_insight = f"\nNote: Focus your answer on '{change_filter}' based on retrieved data.\n"

    fallback_note = ""
    if not context:
        fallback_note = "\n(Note: No indexed data is available yet. Answer based on general market intelligence knowledge.)\n"

    prompt = f"""You are a market intelligence analyst.{system_insight}{fallback_note}

Context:
{context if context else "No indexed competitor data available."}

Question:
{query}

Give a clear, concise answer with insights.
"""

    try:
        response = client_gemini.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return "⏳ API Quota Exceeded (Free Tier). Please wait 60 seconds and try again."
        return f"⚠️ Generate API Error: {str(e)}"


def retrieve_company_context(company_name, k=10):
    """Retrieve Qdrant context for a specific company."""
    if not _qdrant_available or client is None:
        return ""
    try:
        from qdrant_client.http.models import Filter, FieldCondition, MatchValue
        vector = embed_model.encode(
            f"features pricing strategy changes for {company_name}"
        ).tolist()

        query_filter = Filter(
            must=[
                FieldCondition(
                    key="brand",
                    match=MatchValue(value=company_name)
                )
            ]
        )

        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            query_filter=query_filter,
            limit=k
        )

        hits = results.points if hasattr(results, "points") else results
        return "\n\n".join([h.payload["text"] for h in hits[:k]])
    except Exception:
        return ""


def generate_whitespace_analysis(company1: str, company2: str, query: str):
    ctx1 = retrieve_company_context(company1)
    ctx2 = retrieve_company_context(company2)

    prompt = f"""You are an expert market intelligence analyst.
Conduct a Whitespace Detection and Competitive Recommendation Analysis comparing two companies based on the provided datasets and previous trends.

Company 1: {company1}
Dataset/Trends:
{ctx1 if ctx1 else "No indexed data available for this company."}

Company 2: {company2}
Dataset/Trends:
{ctx2 if ctx2 else "No indexed data available for this company."}

User Focus Area: {query}

Instructions:
1. Identify the 'whitespace' (market gaps, missing features, or missing price tiers).
2. Compare the datasets and previous trends of both companies.
3. Provide strategic recommendations on where each company can catch up or outmaneuver the other.
4. Format your output clearly with markdown headers and bullet points.
"""

    try:
        response = client_gemini.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return "⏳ LLM API Quota Exceeded. The system is temporarily rate-limited. Please wait a minute."
        return f"⚠️ LLM Inference Error: {str(e)}"