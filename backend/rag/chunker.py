from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=400,chunk_overlap=150)
    return splitter.split_documents(docs)
