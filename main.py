from fastapi import FastAPI
from rag.faq_rag import generate_answer
from rag.vector_store import build_vector_store

app = FastAPI()

@app.on_event("startup")
def startup_event():
    build_vector_store()

@app.get("/")
def home():
    return {"message": "FAQ RAG API is live!..."}

@app.post("/api/ask-faq")
def ask_faq(question: str):
    answer = generate_answer(question).strip()

    if "not sure" in answer.lower():
        return {"question": question, "answer": answer}

    return {"answer": answer}