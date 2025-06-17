import shutil
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings

embedding=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
VECTOR_DIR="data/faiss_index"

def create_vectorstore(documents):
    # ❌ If the index already exists, remove it first
    if os.path.exists(VECTOR_DIR):
        shutil.rmtree(VECTOR_DIR)

    # ✅ Create fresh FAISS index
    vectorstore = FAISS.from_documents(documents, embedding)

    # Save to new (clean) directory
    os.makedirs(VECTOR_DIR, exist_ok=True)
    vectorstore.save_local(VECTOR_DIR)

def load_vectorstore():
    return FAISS.load_local(VECTOR_DIR,embedding, allow_dangerous_deserialization=True)