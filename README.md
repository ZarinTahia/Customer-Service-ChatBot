# Customer Support Chatbot (MCP + LangGraph + RAG + SQL)
Generative AI powered Multi-Agent System that enables natural language interaction with both structured and unstructured data.
A multi-tool AI chatbot that answers customer support questions using:
- SQL Database (Customers & Tickets)
- Policy Documents (RAG with Chroma)
- LLM-based routing using LangGraph
- MCP Server integration
- Streamlit Web Interface

## Architecture Overview
User (Streamlit UI / MCP Client)
            ↓
        MCP Server
            ↓
      LangGraph Router
            ↓
   ┌───────────────┬───────────────┐
   ↓                               ↓
SQL Tool                       PDF RAG Tool
(SQLite DB)                 (Chroma + Embeddings)

## Features

### 