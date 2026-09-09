import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="ClaimsIQ AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ClaimsIQ Enterprise AI Assistant")

st.write("Ask questions about insurance claims.")

question = st.text_input(
    "Ask a question"
)

if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:

        with st.spinner("Thinking..."):

            response = requests.post(
                API_URL,
                json={
                    "question": question
                }
            )

            if response.status_code == 200:

                answer = response.json()["answer"]

                st.success("Answer")

                st.write(answer)

            else:

                st.error(response.text)