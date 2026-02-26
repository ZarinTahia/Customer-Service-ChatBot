import sys
from pathlib import Path

# Allow imports from project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server.fastmcp import FastMCP
from agents.router_bot import answer

# MCP server
mcp = FastMCP("Customer Service Chatbot")

@mcp.tool()
def chat(question: str) -> str:
    """Route to SQL or RAG agent and return answer."""
    if not question.strip():
        return "Please ask a valid question."
    return answer(question)

# creates HTTP ASGI app
app = mcp.streamable_http_app()