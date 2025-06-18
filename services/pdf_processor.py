from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def process_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # Split pages into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(pages)

    # ✅ Add the source file name to each chunk's metadata
    source_name = os.path.basename(file_path)
    for chunk in chunks:
        chunk.metadata["source"] = source_name

    return chunks
