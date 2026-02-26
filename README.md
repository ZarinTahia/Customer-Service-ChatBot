# 💬 Generative AI Multi-Agent Customer Support System

## Overview

This project implements a **Generative AI–powered Multi-Agent System** that enables natural language interaction with both structured and unstructured data.

The system helps customer support executives retrieve:

- Structured customer data (SQL database)
- Company policy documents (PDF → Vector DB)

The architecture separates frontend and backend using an **MCP (Model Context Protocol) Server**, ensuring clean orchestration between UI, agents, and data sources.


## Architecture

```text
Streamlit UI
    |
    v
MCP Server (HTTP)  [FastMCP + Uvicorn]
    |
    v
LangGraph Router Agent
    |
    +--------------------+--------------------+
    |                    |                    |
    v                    v                    v
SQL Agent           RAG Agent              LLM
(Structured)        (Unstructured PDFs)    (Answer generation)
    |                    |
    v                    v
SQL Database          Vector DB
(SQLite/Postgres)     (Chroma/FAISS)

```
### Components

- **Streamlit** → User interface
- **MCP Server** → Exposes `chat()` tool and orchestrates requests
- **LangGraph Router Agent** → Decides which data source to use
- **SQL Database** → Stores structured customer data
- **Vector Database** → Stores embedded company policy PDFs
- **LLM** → Generates context-aware responses

---
## Features

- Upload and process company policy PDFs
- Query structured customer profiles via natural language
- Retrieve past support ticket summaries
- Generate contextual policy explanations
- Multi-agent routing (SQL vs RAG)
- MCP-based backend architecture

---

## How It Works

1. User submits a query via Streamlit.
2. Streamlit sends the query to the MCP Server.
3. MCP exposes a tool: `chat(question)`.
4. The tool calls the LangGraph router agent.
5. The router decides:
   - SQL Agent → For customer profile/ticket queries
   - RAG Agent → For policy/document queries
6. LLM generates final response.
7. Response is returned to the UI.

---

## Technology Stack

- **LLM:** OpenAI / compatible model
- **Embeddings:** OpenAI / HuggingFace
- **Frameworks:** LangChain, LangGraph
- **Structured Data:** SQL Database (SQLite / PostgreSQL)
- **Unstructured Data:** Vector DB (Chroma / FAISS)
- **Server:** MCP (Model Context Protocol)
- **UI:** Streamlit
- **Backend Server:** FastMCP + Uvicorn

---

## Project Structure

