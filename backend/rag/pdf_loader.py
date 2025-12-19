import os
from pypdf import PdfReader
from langchain_core.documents import Document
from .chunker import split_text
from .vectorstore import get_vectorstore


async def process_pdf(file):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(temp_path)
    docs = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            docs.append(Document(page_content=text))

    chunks = split_text(docs)
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)

    os.remove(temp_path)
