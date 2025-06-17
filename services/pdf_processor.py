from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_pdf(file_path: str):
    loader=PyPDFLoader(file_path)
    pages=loader.load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    return splitter.split_documents(pages)

