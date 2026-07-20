import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool
from src.config import POLICIES_DIR, CHROMA_DB_DIR

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_store():
    """Loads existing Chroma vector store or creates one if it doesn't exist."""
    if os.path.exists(CHROMA_DB_DIR) and os.listdir(CHROMA_DB_DIR):
        print("Loading existing Chroma vector store...")
        return Chroma(persist_directory=str(CHROMA_DB_DIR), embedding_function=embeddings)

    print("Initializing Chroma vector store from HR policy PDFs...")
    loader = PyPDFDirectoryLoader(str(POLICIES_DIR))
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    splits = text_splitter.split_documents(docs)

    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )
    print("Vector store initialized successfully.")
    return vector_store

vector_store = get_vector_store()
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

@tool
def query_policy_documents(query: str) -> str:
    """
    Queries the official HR policy documents.
    Use this tool to answer questions about rules, regulations, annual leave,
    remote work, performance reviews, code of conduct, and training development.
    Input MUST be a clear, specific search query.
    """
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant policy information found."

    context = "\n\n".join([f"--- Excerpt {i+1} ---\n{doc.page_content}" for i, doc in enumerate(docs)])
    return context
