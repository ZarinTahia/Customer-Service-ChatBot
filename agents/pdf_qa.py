from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
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

    endpoint = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        provider="together",
        task="conversational",
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        temperature=0.1,
        max_new_tokens=256,
    )
    llm = ChatHuggingFace(llm=endpoint)

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