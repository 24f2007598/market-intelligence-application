from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from google import genai
import os
from dotenv import load_dotenv
load_dotenv(override=True)
# from scripts.structured_extraction import extract_structured_data
# from scripts.csv_writer import save_to_csv
from utils.config import COLLECTION_NAME
from db.db import engine
from sqlalchemy import text


# 🔹 Gemini setup (NEW SDK)
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 🔹 Qdrant
client = QdrantClient("localhost", port=6333)

# 🔹 Embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_context(query, k=5, change_filter=None):
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

    # ✅ FIXED SQL
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT cleaned_text FROM documents ORDER BY id DESC LIMIT 3")
        ).fetchall()

    postgres_context = "\n\n".join([r[0] for r in rows])

    return qdrant_context + "\n\n" + postgres_context

def generate_answer(query:str, change_filter=None):
    context = retrieve_context(query, change_filter=change_filter)

    system_insight = ""
    if change_filter:
        system_insight = f"\nNote: The user is specifically asking about a '{change_filter}'. Focus your answer on this aspect based on the retrieved data.\n"

    prompt = f"""
You are a market intelligence analyst.{system_insight}

Context:
{context}

Question:
{query}

Give a clear, concise answer with insights.
"""

    try:
        response = client_gemini.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return "⏳ API Quota Exceeded (Free Tier). Please wait 60 seconds and try again."
        return f"⚠️ Generate API Error: {str(e)}"


def retrieve_company_context(company_name, k=10):
    from qdrant_client.http.models import Filter, FieldCondition, MatchValue
    vector = embed_model.encode(f"features pricing strategy changes for {company_name}").tolist()
    
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


def generate_whitespace_analysis(company1: str, company2: str, query: str):
    ctx1 = retrieve_company_context(company1)
    ctx2 = retrieve_company_context(company2)
    
    prompt = f"""
You are an expert market intelligence analyst. 
Conduct a Whitespace Detection and Competitive Recommendation Analysis comparing two companies based on the provided datasets and previous trends.

Company 1: {company1}
Dataset/Trends: 
{ctx1}

Company 2: {company2}
Dataset/Trends:
{ctx2}

User Focus Area: {query}

Instructions:
1. Identify the 'whitespace' (market gaps, missing features, or missing price tiers).
2. Compare the datasets and previous trends of both companies.
3. Provide strategic recommendations on where each company can catch up or outmaneuver the other.
4. Format your output clearly with markdown headers and bullet points.
"""

    try:
        response = client_gemini.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return "⏳ LLM API Quota Exceeded. The system is temporarily rate-limited. Please wait a minute."
        return f"⚠️ LLM Inference Error: {str(e)}"

# def run_rag(query, llm):
#     rag_output = your_existing_rag_logic(query)

#     # 🔥 PASS QUERY HERE
#     structured_data = extract_structured_data(llm, query, rag_output)

#     save_to_csv(structured_data)

#     return rag_output

# if __name__ == "__main__":
#     while True:
#         q = input("\nAsk: ")
#         print("\nAnswer:\n", ask(q))


# from qdrant_client import QdrantClient
# from sentence_transformers import SentenceTransformer
# import google.generativeai as genai
# import os

# from utils.config import COLLECTION_NAME
# from db.db import engine

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# client = QdrantClient("localhost", port=6333)
# embed_model = SentenceTransformer("all-MiniLM-L6-v2")


# def retrieve_context(query, k=5):
#     vector = embed_model.encode(query).tolist()

#     results = client.search(
#         collection_name=COLLECTION_NAME,
#         query_vector=vector,
#         limit=k
#     )

#     qdrant_context = "\n\n".join([r.payload["text"] for r in results])

#     # 🔥 add postgres latest docs
#     with engine.connect() as conn:
#         rows = conn.execute(
#             "SELECT cleaned_text FROM documents ORDER BY id DESC LIMIT 3"
#         ).fetchall()

#     postgres_context = "\n\n".join([r[0] for r in rows])

#     return qdrant_context + "\n\n" + postgres_context


# def ask(query):
#     context = retrieve_context(query)

#     prompt = f"""
# You are a market intelligence analyst.

# Context:
# {context}

# Question:
# {query}

# Answer clearly with insights.
# """

#     response = model.generate_content(prompt)
#     return response.text


# if __name__ == "__main__":
#     while True:
#         q = input("\nAsk: ")
#         print("\nAnswer:\n", ask(q))


# from qdrant_client import QdrantClient
# from sentence_transformers import SentenceTransformer
# import google.generativeai as genai
# import os

# # 🔹 Setup Gemini
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# # 🔹 Setup Qdrant
# client = QdrantClient("localhost", port=6333)

# # 🔹 Embedding model
# embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# COLLECTION = "market_intel"


# def retrieve_context(query, k=5):
#     vector = embed_model.encode(query).tolist()

#     results = client.search(
#         collection_name=COLLECTION,
#         query_vector=vector,
#         limit=k
#     )

#     context = "\n\n".join([r.payload["text"] for r in results])
#     return context


# def ask(query):
#     context = retrieve_context(query)

#     prompt = f"""
# You are a market intelligence analyst.

# Answer the question using ONLY the context below.

# Context:
# {context}

# Question:
# {query}

# Give a clear, concise, insight-driven answer.
# """

#     response = model.generate_content(prompt)
#     return response.text


# if __name__ == "__main__":
#     while True:
#         q = input("\nAsk: ")
#         print("\nAnswer:\n", ask(q))