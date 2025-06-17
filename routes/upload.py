from fastapi import APIRouter, UploadFile, File
import shutil
import os

from services.pdf_processor import process_pdf
from services.vectorstore import create_vectorstore
from services.memory import memory

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)

    # Always extract clean filename
    filename = os.path.basename(file.filename)
    file_path = os.path.join("temp", filename)

    # ✅ This reads the actual binary contents of the uploaded PDF file
    contents = await file.read()
    
    # Save to disk
    with open(file_path, "wb") as f:
        f.write(contents)

    # 🔒 Validate PDF is not empty or corrupted
    if os.path.getsize(file_path) == 0:
        return {"error": "Uploaded file is empty or corrupted."}

    try:
        print("📄 Processing PDF:", file_path)
        documents = process_pdf(file_path)
        print(f"🧾 Extracted {len(documents)} chunks from PDF.")

        create_vectorstore(documents)
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}
    finally:
        os.remove(file_path)

    return {"message": "✅ PDF processed and vectorstore created."}
