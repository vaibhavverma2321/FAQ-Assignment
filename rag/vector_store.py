import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from rag.embeddings import embeddings

load_dotenv()

COLLECTION_NAME = "clinic_faq"
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vectordb")
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "clinic_info.json"


def _get_vector_store():
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
    )

def build_vector_store():
    vector_store = _get_vector_store()
    existing_items = vector_store.get(include=[])
    if existing_items.get("ids"):
        print("Vector store already exists; skipping rebuild.")
        return

    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    texts = []
    metadatas = []
    ids = []

    i = 0
    for section, faqs in data.items():
        for faq in faqs:
            question = faq.get("q")
            answer = faq.get("a")

            texts.append(answer)
            metadatas.append({"question": question, "category": section})
            ids.append(str(i))
            i += 1

    vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)

    print(f"Vector store built successfully with {i} FAQs!")

def get_relevant_context(query, top_k=3):
    vector_store = _get_vector_store()
    results = vector_store.similarity_search(
        query=query,
        k=top_k
    )

    return [doc.page_content for doc in results]
