#FAST API entry point

from fastapi import FastAPI
from routes import upload,query

app=FastAPI(title="pdfchatbot")

app.include_router(upload.router)
app.include_router(query.router)

