# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class QueryRequest(BaseModel):
#     query: str

# @app.get("/")
# def home():
#     return {"status": "API running"}

from fastapi import FastAPI
from pydantic import BaseModel
from scripts.rag import generate_answer

app = FastAPI()


class QueryRequest(BaseModel):
    query: str

class WhitespaceRequest(BaseModel):
    company1: str
    company2: str
    query: str

@app.get("/")
def home():
    return {"status": "API running"}


@app.post("/rag")
def rag_endpoint(req: QueryRequest):
    answer = generate_answer(req.query)
    return {"answer": answer}

@app.post("/whitespace")
def whitespace_endpoint(req: WhitespaceRequest):
    from scripts.rag import generate_whitespace_analysis
    answer = generate_whitespace_analysis(req.company1, req.company2, req.query)
    return {"answer": answer}

# @app.post("/query")
# def query_rag(request: QueryRequest):
#     result = run_rag(request.query, llm)
#     return {"response": result}    