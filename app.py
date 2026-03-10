import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom UI style
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}
h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
}
</style>
""", unsafe_allow_html=True)

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to read PDF
def read_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Function to ask AI
def ask_ai(question, pdf_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer questions using the provided PDF context."},
            {"role": "user", "content": f"Context: {pdf_text}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content

# Title
st.title("🤖 AI PDF Chatbot")
st.write("Upload a PDF and ask questions about the document.")

st.divider()

# **Mobile-friendly file uploader on main page**
uploaded_file = st.file_uploader(
    "📂 Upload your PDF",
    type="pdf",
    accept_multiple_files=False
)

if uploaded_file:
    with st.spinner("Reading PDF..."):
        pdf_text = read_pdf(uploaded_file)
    st.success("✅ PDF Loaded Successfully!")

    question = st.text_input("💬 Ask a question from the PDF")

    if st.button("🔍 Get Answer"):
        if question.strip() == "":
            st.warning("Please enter a question before submitting.")
        else:
            with st.spinner("AI is thinking..."):
                answer = ask_ai(question, pdf_text)
            st.subheader("📄 Answer")
            st.write(answer)

st.divider()
st.caption("Built by Lakshana | AI PDF Chatbot Project")
