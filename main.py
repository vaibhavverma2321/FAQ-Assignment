from fastapi import FastAPI, HTTPException
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
    try:
        answer = generate_answer(question).strip()
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    if "not sure" in answer.lower():
        return {"question": question, "answer": answer}

    return {"answer": answer}
