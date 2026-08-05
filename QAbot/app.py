import os
import streamlit as st

from dotenv import load_dotenv
from openai import OpenAI

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# -----------------------------
# OpenRouter Client
# -----------------------------

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="PDF Chatbot")

st.title("📄 PDF Question Answer Bot")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# -----------------------------
# Process PDF
# -----------------------------

if uploaded_file:

    os.makedirs("uploads", exist_ok=True)

    pdf_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded Successfully")

    if st.button("Create Knowledge Base"):

        with st.spinner("Processing PDF..."):

            # Load PDF
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            # Split
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100
            )

            chunks = splitter.split_documents(
                documents
            )

            # Embeddings
            embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # Create Vector DB
            vector_db = Chroma.from_documents(
                documents=chunks,
                embedding=embedding_model,
                persist_directory="./chroma_db"
            )

        st.success(
            f"Knowledge Base Created ({len(chunks)} chunks)"
        )

# -----------------------------
# Ask Question
# -----------------------------

question = st.text_input(
    "Ask a Question"
)

if question:

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embedding_model
    )

    docs = db.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a helpful assistant.

Answer only from the provided context.

If answer is not present,
say:
"I could not find that information in the document."

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    st.subheader("Answer")

    st.write(answer)