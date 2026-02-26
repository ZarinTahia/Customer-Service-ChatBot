from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

CHROMA_DIR = Path("db/chroma_policies")

def answer_pdf(question: str) -> str:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name="policies",
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    # Groq chat model 
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.4,
        max_tokens=256,
        api_key=os.getenv("GROQ_API_KEY"),  # env var is set
    )

    prompt = ChatPromptTemplate.from_template("""
Use only the context to answer the question.
If you don't know the answer from the context, say "I don't know."

Context:
{context}

Question: {question}

Start the answer directly. No small talk.
""".strip())

    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])

    msg = llm.invoke(prompt.format_messages(question=question, context=context))
    return msg.content.strip()

def main():
    question = "tell me about core principals?"
    print(answer_pdf(question))

if __name__ == "__main__":
    main()