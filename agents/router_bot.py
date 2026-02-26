from dotenv import load_dotenv
load_dotenv()

import os
from typing import TypedDict, Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

from agents.sql_agent import answer_question as answer_sql
from agents.pdf_qa import answer_pdf


# State 
class BotState(TypedDict):
    question: str
    route: Literal["sql", "pdf", "clarify"]
    answer: str


# LLM Router (Groq) 
router_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,          # routing should be deterministic
    max_tokens=10,            # only need "sql" or "pdf"
    api_key=os.getenv("GROQ_API_KEY"),  # optional if env var is set
)

router_prompt = ChatPromptTemplate.from_template("""
You are a routing assistant.

Choose exactly ONE tool:

- "sql" → for questions about customers, profiles, tickets, counts, cities, status, or database information.
- "pdf" → for questions about policies, refund rules, code of conduct, privacy, terms, guidelines, handbook.

Do NOT explain.
Return ONLY one word: sql OR pdf.

User question: {question}
""")


def router_node(state: BotState) -> BotState:
    q = state["question"]
    msg = router_llm.invoke(router_prompt.format_messages(question=q))
    decision = (msg.content or "").strip().lower()

    # Guardrails: accept only valid labels
    if decision not in ("sql", "pdf", "clarify"):
        # sensible fallback: vague -> clarify, else sql
        if len(q.split()) <= 4:
            decision = "clarify"
        else:
            decision = "sql"

    return {"question": q, "route": decision, "answer": ""}


def clarify_node(state: BotState) -> BotState:
    q = state["question"]
    followup = (
        "I can help, but I need a bit more detail. Do you mean:\n"
        "1) total number of customers,\n"
        "2) recent ticket volume/priority,\n"
        "3) a specific customer’s profile?\n"
        "4) Phone number of Zarin?\n"
        "5) How many tickets Zarin bought?\n"
        "If it’s a specific customer, please tell me their name."
    )
    return {**state, "answer": followup}


def sql_node(state: BotState) -> BotState:
    ans = answer_sql(state["question"])
    return {**state, "answer": ans}


def pdf_node(state: BotState) -> BotState:
    ans = answer_pdf(state["question"])
    return {**state, "answer": ans}


def next_step(state: BotState) -> str:
    return state["route"]


# LangGraph 
graph = StateGraph(BotState)
graph.add_node("router", router_node)
graph.add_node("clarify", clarify_node)
graph.add_node("sql", sql_node)
graph.add_node("pdf", pdf_node)

graph.set_entry_point("router")
graph.add_conditional_edges(
    "router",
    next_step,
    {"sql": "sql", "pdf": "pdf", "clarify": "clarify"},
)

graph.add_edge("sql", END)
graph.add_edge("pdf", END)
graph.add_edge("clarify", END)

app = graph.compile()


# Convenience function for UI 
def answer(question: str) -> str:
    out = app.invoke({"question": question, "route": "sql", "answer": ""})
    return out["answer"]


# test 
if __name__ == "__main__":
    tests = [
        "Can you summarise the code of conduct?",
        "How many tickets does Ava Patel have?",
        "Where does Ava Patel live?",
        "What is the refund policy?",
        "How is our customer?"
    ]
    for q in tests:
        out = app.invoke({"question": q, "route": "sql", "answer": ""})
        print("\nQ:", q)
        print("Route:", out["route"])
        print("A:", out["answer"])