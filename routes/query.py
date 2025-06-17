from fastapi import APIRouter, Query
from services.vectorstore import load_vectorstore
from services.llm import get_llm
from langchain.chains import RetrievalQA

router = APIRouter()

@router.get("/query")
def ask_question(q: str = Query(...)):
    retriever = load_vectorstore().as_retriever(search_kwargs={"k": 5})
    llm = get_llm()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa_chain.run(q)
    return {"answer": result}
