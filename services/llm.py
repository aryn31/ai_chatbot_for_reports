from langchain_community.llms import Ollama

def get_llm():
    return Ollama(
        model="mistral",   # must match the model name you’ve pulled in Ollama
        temperature=0.7
    )
