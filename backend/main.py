from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from rag.pdf_loader import process_pdf
from rag.qa import answer_question
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile):
    await process_pdf(file)
    return {"status": "File uploaded and processed successfully"}

@app.post("/ask")
async def ask(payload: dict):
    question = payload["question"]
    history = payload.get("history", [])
    answer = answer_question(question, history)
    return {"answer": answer}

