from fastapi import APIRouter, Query
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from services.vectorstore import load_vectorstore
from services.llm import get_llm
from services.memory import memory

router = APIRouter()

# Prompt template with chat history
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant answering questions based on the following context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

llm = get_llm()

# Load retriever
def get_retriever():
    return load_vectorstore().as_retriever(search_kwargs={"k": 100})

# Format retrieved docs to string
# def format_docs(docs):
#     print(f"📄 Retrieved {len(docs)} docs")
#     return "\n\n".join(doc.page_content for doc in docs)

def format_docs(docs):
    for i, doc in enumerate(docs):
        print(f"🔹 Doc {i+1}: {doc.page_content[:200]}...\n")
    return "\n\n".join(doc.page_content for doc in docs)

@router.get("/query")
def query(q: str = Query(...)):
    print(f"🤖 User Question: {q}")

    # Save user input to memory
    memory.chat_memory.add_user_message(q)
    chat_history = memory.chat_memory.messages

    try:
        retriever = get_retriever()

        # Define the RAG chain
        rag_chain = (
            RunnableLambda(lambda x: {
                "context": format_docs(retriever.get_relevant_documents(x["question"])),
                "question": x["question"],
                "chat_history": x["chat_history"]
            })
            | prompt
            | llm
            | StrOutputParser()
        )
        print("using rag pipeline")
        # Invoke chain
        answer = rag_chain.invoke({
            "question": q,
            "chat_history": chat_history
        })

    except Exception as e:
        print("❌ Error during RAG pipeline:", str(e))
        return {"error": f"❌ Error during RAG pipeline: {str(e)}"}

    # Save LLM response
    memory.chat_memory.add_ai_message(answer)
    print(f"✅ Answer: {answer}")
    return {"answer": answer}
