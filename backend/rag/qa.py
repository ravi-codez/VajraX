from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from .vectorstore import get_vectorstore

def format_history(history):
    conversation = ""
    for msg in history[:-1]:  # exclude current question
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"
    return conversation

def answer_question(query, history):
    db = get_vectorstore()
    retriever = db.as_retriever(search_type="mmr",search_kwargs={"k": 3,"lambda_mult": 0.5})

    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join(d.page_content for d in docs)

    conversation_history = format_history(history)

    prompt = PromptTemplate(
        template="""
You are a helpful assistant that answers questions using the PDF context
and the previous conversation. if the context is not sufficient to give 
answers then simply response i do not know based on the given context

Conversation History:
{history}

Context:
{context}

Current Question:
{question}

Answer:
""",
        input_variables=["history", "context", "question"]
    )

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    return llm.predict(
        prompt.format(
            history=conversation_history,
            context=context,
            question=query
        )
    )
