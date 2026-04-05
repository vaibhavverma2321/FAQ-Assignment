from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from rag.vector_store import get_relevant_context

load_dotenv()

_GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
_CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")

def _is_model_not_found_error(error: Exception) -> bool:
    message = str(error).lower()
    return "not found" in message and "generatecontent" in message


def _make_client(model_name: str):
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=_GOOGLE_API_KEY,
    )

def generate_answer(question: str):
    context_docs = get_relevant_context(question)
    context = "\n".join(context_docs)

    prompt = f"""
You are a helpful and factual medical clinic assistant.
Answer the user's question using ONLY the information in the context below.

If the answer is not in the context, say exactly:
"I'm not sure about that."

Important:
- Do NOT include the question in your response.
- Do NOT use JSON, brackets, or keys like "question" or "answer".
- Reply ONLY with the plain answer sentence.

Context:
{context}

Question: {question}
"""

    model_candidates = []
    for model_name in (_CHAT_MODEL, "gemini-2.5-flash"):
        if model_name not in model_candidates:
            model_candidates.append(model_name)

    last_error = None
    for model_name in model_candidates:
        try:
            response = _make_client(model_name).invoke(
                [
                    ("system", "You are a friendly, concise clinic assistant."),
                    ("human", prompt),
                ]
            )
            return response.content.strip()
        except Exception as error:
            last_error = error
            if not _is_model_not_found_error(error):
                raise

    raise RuntimeError("No supported Gemini chat model is available.") from last_error
