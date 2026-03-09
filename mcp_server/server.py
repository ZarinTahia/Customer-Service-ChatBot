# mcp_server/server.py

import sys
from pathlib import Path
import json
from dotenv import load_dotenv

load_dotenv()

# Allow imports from project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server.fastmcp import FastMCP
from langchain_groq import ChatGroq

# Your existing agents
from agents.sql_agent import answer_question as answer_sql
from agents.pdf_qa import answer_pdf

# ---------------------------
# 1️⃣ Define the LLM
# ---------------------------
groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",  # or your Groq model
    temperature=0.0,                # deterministic routing
    max_tokens=100,                  # enough to return tool names
    api_key=None                      # optional if GROQ_API_KEY is set
)

# ---------------------------
# Define the available tools
# ---------------------------
TOOLS = {
    "sql": answer_sql,
    "pdf": answer_pdf
}

# ---------------------------
# Create MCP server
# ---------------------------
mcp = FastMCP("Customer Service Chatbot")

# ---------------------------
# Define the Groq prompt template
# ---------------------------
ROUTING_PROMPT = """
You are a smart assistant that can call multiple tools to answer a user's question.
Available tools:

- sql: answers questions about customer data, tickets, profiles, cities, etc.
- pdf: answers questions about company policies, guidelines, refund rules, handbook, etc.

For the following user question:
"{question}"

Decide which tool(s) are needed. You may choose one or both.

Return a JSON object with this format:

{{
  "tools": ["sql","pdf"],  # list only the tools needed
  "sub_questions": ["...", "..."]  # question(s) to send to each tool, in the same order
}}

Do NOT add explanations.
"""

# ---------------------------
# Define MCP tool
# ---------------------------
@mcp.tool()
def chat(question: str) -> str:
    """
    Main chat tool exposed via MCP.
    Groq decides which internal tools (sql, pdf) to call.
    Returns the combined answer.
    """
    if not question.strip():
        return "Please ask a valid question."

    # Ask Groq which tools to use
    msg = groq_llm.invoke(ROUTING_PROMPT.format(question=question))
    content = (msg.content or "").strip()

    # Parse Groq JSON response
    try:
        routing = json.loads(content)
        tools_to_call = routing.get("tools", [])
        sub_questions = routing.get("sub_questions", [])
    except json.JSONDecodeError:
        # fallback: call both tools with full question
        tools_to_call = ["sql", "pdf"]
        sub_questions = [question] * 2

    # Execute tools
    final_answer = ""
    for tool_name, q_part in zip(tools_to_call, sub_questions):
        tool_func = TOOLS.get(tool_name)
        if tool_func:
            try:
                ans = tool_func(q_part)
                final_answer += f"{ans}\n"
            except Exception as e:
                final_answer += f" Error: {str(e)}\n"

    if not final_answer:
        final_answer = "Sorry, I could not find an answer."

    return final_answer.strip()

# Create ASGI app

app = mcp.streamable_http_app()


# run server via uvicorn

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mcp_server.server:app", host="127.0.0.1", port=8000, reload=True)