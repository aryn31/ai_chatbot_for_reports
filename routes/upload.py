from fastapi import APIRouter,UploadFile,File
import os
from services.pdf_processor import process_pdf
from services.vectorstore import create_vectorstore

router=APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("temp",exist_ok=True)
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    documents = process_pdf(file_path)
    create_vectorstore(documents)
    os.remove(file_path)

    return {"message": "PDF processed and vectorstore created."}