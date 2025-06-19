import shutil
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings

# embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
embedding = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")
VECTOR_DIR = "data/faiss_index"

def create_vectorstore(documents):
    # ❌ Delete old index if exists
    if os.path.exists(VECTOR_DIR):
        shutil.rmtree(VECTOR_DIR)
        print("🗑️ Old vectorstore removed.")

    # ✅ Create and save new index
    vectorstore = FAISS.from_documents(documents, embedding)
    os.makedirs(VECTOR_DIR, exist_ok=True)
    vectorstore.save_local(VECTOR_DIR)
    print("✅ New vectorstore created and saved.")

def load_vectorstore():
    print("📦 Loading vectorstore from:", VECTOR_DIR)
    return FAISS.load_local(VECTOR_DIR, embedding, allow_dangerous_deserialization=True)
