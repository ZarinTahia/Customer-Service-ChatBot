import sys
from pathlib import Path

# Make project root importable (so "import agents..." works in mcp dev)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server.fastmcp import FastMCP
from agents.router_bot import answer

mcp = FastMCP("Customer Support Chatbot")

@mcp.tool()
def chat(question: str) -> str:
    """Answer questions using SQL + PDF RAG routed by LangGraph."""
    return answer(question)

if __name__ == "__main__":
    mcp.run()
    