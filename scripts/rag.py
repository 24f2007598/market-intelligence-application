from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from google import genai
import os

from utils.config import COLLECTION_NAME
from db.db import engine
from sqlalchemy import text


# 🔹 Gemini setup (NEW SDK)
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 🔹 Qdrant
client = QdrantClient("localhost", port=6333)

# 🔹 Embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")



def retrieve_context(query, k=5):
    vector = embed_model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
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

def generate_answer(query:str):
    context = retrieve_context(query)

    prompt = f"""
You are a market intelligence analyst.

Context:
{context}

Question:
{query}

Give a clear, concise answer with insights.
"""

    response = client_gemini.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text


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