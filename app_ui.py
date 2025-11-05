import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Clinic Assistant", page_icon="🏥", layout="centered")

st.title("🏥 Clinic Assistant Chatbot")
st.write("Ask me anything about the clinic, billing, or policies.")

user_input = st.text_input("Your Question:", "")

if st.button("Ask"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{BASE_URL}/api/ask-faq",
                    params={"question": user_input}
                )

                if response.status_code == 200:
                    result = response.json()
                    if "answer" in result:
                        st.markdown(f"**Assistant:** {result['answer']}")
                    else:
                        st.markdown("No response received from the assistant.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
