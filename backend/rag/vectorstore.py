from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    return Chroma(
        persist_directory="chroma_store",
        embedding_function=embeddings
    )
