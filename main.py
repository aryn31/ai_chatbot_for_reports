#FAST API entry point
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import upload,query
import multiprocessing as mp
mp.set_start_method('spawn', force=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    yield
    # Shutdown - cleanup multiprocessing resources
    try:
        # Clean up any remaining multiprocessing resources
        if hasattr(mp.resource_tracker, '_resource_tracker'):
            mp.resource_tracker._resource_tracker._stop()
    except Exception as e:
        print(f"Error during cleanup: {e}")

app=FastAPI(title="pdfchatbot")

app.include_router(upload.router)
app.include_router(query.router)

# 👇 Add this block at the bottom of the file
if __name__ == "__main__":

    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
