from openai import OpenAI
from dotenv import load_dotenv
import os
from rag.vector_store import get_relevant_context

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly, concise clinic assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content.strip()
    return answer
