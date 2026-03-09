import streamlit as st
from PyPDF2 import PdfReader
import openai

# Add your API key here
openai.api_key = "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"
kA"

def read_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def ask_ai(question, pdf_text):
    response = openai.chat.completions.create(   # <-- UPDATED method
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{question}\nContext: {pdf_text}"}
        ]
    )
    return response.choices[0].message.content
st.title("AI PDF Chatbot")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    pdf_text = read_pdf(uploaded_file)
    st.success("PDF Loaded!")

    question = st.text_input("Ask a question about the PDF")

    if st.button("Get Answer"):
        answer = ask_ai(question, pdf_text)

        st.write(answer)

