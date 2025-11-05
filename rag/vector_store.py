import chromadb
from chromadb.config import Settings
from rag.embeddings import get_embedding
import json, os

class OpenAIEmbeddingFunction:
    def embed_documents(self, input):
        return [get_embedding(text) for text in input]

    def embed_query(self, input):
        return [get_embedding(input)]

    def __call__(self, input):
        return self.embed_documents(input)

    def name(self):
        return "openai-embedding-function"

def build_vector_store():
    client = chromadb.Client(Settings(
        persist_directory=os.getenv("VECTOR_DB_PATH"),
        anonymized_telemetry=False
    ))

    embedding_function = OpenAIEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="clinic_faq",
        embedding_function=embedding_function
    )

    with open("data/clinic_info.json") as f:
        data = json.load(f)

    i = 0
    for section, faqs in data.items():
        for faq in faqs:
            question = faq.get("q")
            answer = faq.get("a")

            collection.add(
                documents=[answer],
                metadatas=[{"question": question, "category": section}],
                ids=[str(i)]
            )
            i += 1

    print(f"✅ Vector store built successfully with {i} FAQs!")

def get_relevant_context(query, top_k=3):
    client = chromadb.Client(Settings(
        persist_directory=os.getenv("VECTOR_DB_PATH"),
        anonymized_telemetry=False
    ))

    embedding_function = OpenAIEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="clinic_faq",
        embedding_function=embedding_function
    )

    results = collection.query(query_texts=[query], n_results=top_k)
    return [doc for doc in results["documents"][0]]
