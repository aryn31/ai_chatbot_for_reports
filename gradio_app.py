import gradio as gr
import requests
import mimetypes
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

API_URL = "http://localhost:8000"

uploaded_pdf_path = None  # Global state

def export_chat(chat_history):
    lines = []
    for message in chat_history:
        role = message.get("role", "unknown").capitalize()
        content = message.get("content", "")
        lines.append(f"{role}: {content}\n\n")

    filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.writelines(lines)

    return filename

        
def upload_pdf(file):
    global uploaded_pdf_path
    if file is None:
        return "❌ No file selected."
    
    with open(file.name, "rb") as f:
        file_bytes = f.read()

    # files = {'file': (file.name, file_bytes, 'application/pdf')}
    mime_type, _ = mimetypes.guess_type(file.name)
    files = {'file': (file.name, file_bytes, mime_type or 'application/octet-stream')}
    response = requests.post(f"{API_URL}/upload", files=files)

    if response.status_code == 200:
        uploaded_pdf_path = "✅"
        return response.json().get("message", "✅ Uploaded.")
    else:
        return f"❌ Upload failed: {response.text}"



def chatbot_fn(message, chat_history):
    if not uploaded_pdf_path:
        return "❌ Please upload a PDF first."
    response = requests.get(f"{API_URL}/query", params={"q": message})
    if response.status_code == 200:
        return response.json().get("answer", "No answer found.")
    else:
        return "❌ Failed to get answer."


with gr.Blocks() as demo:
    gr.Markdown("# 🧠 PDF Q&A Chatbot with RAG")

    with gr.Row():
        file_input = gr.File(label="📄 Upload PDF", file_types=[".pdf",".docx"])
        upload_status = gr.Textbox(label="Upload Status", interactive=False)
        upload_btn = gr.Button("Upload PDF")

    chat = gr.ChatInterface(
        fn=chatbot_fn,
        chatbot=gr.Chatbot(label="📘 Ask about your PDF",type='messages'),
        textbox=gr.Textbox(placeholder="Ask a question...", container=False),
        title="PDF Assistant",
        description="Ask questions from your uploaded PDF report.",
    )

    export_btn=gr.Button("⬇️ Export Chat")
    download_file=gr.File(label="Download Chat")

    upload_btn.click(fn=upload_pdf, inputs=file_input, outputs=upload_status)
    export_btn.click(fn=export_chat, inputs=chat.chatbot, outputs=download_file)

demo.launch()
