#FAST API entry point

from fastapi import FastAPI
from routes import upload,query

app=FastAPI(title="pdfchatbot")

app.include_router(upload.router)
app.include_router(query.router)

# 👇 Add this block at the bottom of the file
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
