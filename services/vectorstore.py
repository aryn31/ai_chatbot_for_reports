import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings

embedding=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
VECTOR_DIR="data/faiss_index"

def create_vectorstore(documents):
    vectorstore=FAISS.from_documents(documents,embedding)
    os.makedirs(VECTOR_DIR,exist_ok=True)
    vectorstore.save_local(VECTOR_DIR)

def load_vectorstore():
    return FAISS.load_local(VECTOR_DIR,embedding)