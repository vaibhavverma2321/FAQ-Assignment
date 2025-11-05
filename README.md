🏥 Clinic FAQ Chatbot (FAQ-Assignment)

This project is a simple FAQ chatbot built for a medical clinic.
It allows users to ask questions related to clinic timings, billing, policies, and visit preparation.
The system uses FastAPI as the backend, Streamlit for the UI, and ChromaDB for storing and retrieving relevant FAQ data.
It integrates with the OpenAI API to generate accurate, context-based responses.

🎬 Demo Video
https://github.com/vaibhavverma2321/FAQ-Assignment/releases/tag/FAQ-Assignment-Video

🚀 Features

Interactive chatbot interface for clinic FAQs

Retrieval-Augmented Generation (RAG) setup using ChromaDB

FastAPI backend for handling queries

Streamlit frontend for user interaction

Environment-based configuration for API keys and local URLs

Uses cheaper OpenAI models for cost efficiency

🧩 Tech Stack

Python 3.12+

FastAPI – for backend API

Streamlit – for web UI

ChromaDB – as the vector database

OpenAI API – for embeddings and responses

dotenv – for managing environment variables

⚙️ Setup Instructions
1. Clone the Repository
git clone https://github.com/<your-username>/FAQ-Assignment.git
cd FAQ-Assignment

2. Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Create a .env File

Create a .env file in the root directory and add the following:

OPENAI_API_KEY=your_openai_api_key
VECTOR_DB_PATH=./data/vectordb
BASE_URL=http://localhost:8000

5. Run the FastAPI Server
uvicorn main:app --reload

6. Run the Streamlit App

In a separate terminal:

streamlit run app_ui.py

💬 Example Questions

What are your clinic's hours of operation?

Where is the clinic located?

What insurance providers do you accept?

What should I bring for my appointment?

What is your cancellation policy?

📁 Project Structure
FAQ-Assignment/
│
├── rag/
│   ├── embeddings.py
│   ├── vector_store.py
│   └── faq_rag.py
│
├── data/
│   └── clinic_info.json
│
├── main.py              # FastAPI backend
├── app_ui.py            # Streamlit interface
├── requirements.txt
└── .env.example

🧠 How It Works

All clinic FAQs are stored in a local JSON file.

The data is embedded and stored in a Chroma vector database.

When a user asks a question, the app retrieves the most relevant FAQ context.

The OpenAI API generates an answer only based on that context.

If the answer isn't found, it politely says:

"I'm not sure about that."

📜 License

This project is open-source and available under the MIT License.