import streamlit as st
from PyPDF2 import PdfReader
import openai

# Add your API key here
openai.api_key = "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"

def read_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def ask_ai(question, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": context + "\nQuestion:" + question}
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