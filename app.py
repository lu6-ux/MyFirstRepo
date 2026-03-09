import streamlit as st

from PyPDF2 import PdfReader
from openai import OpenAI


# Read API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def read_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def ask_ai(question, pdf_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions from a PDF."},
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
