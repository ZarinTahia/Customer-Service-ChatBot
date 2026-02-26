# 💬 Generative AI Multi-Agent Customer Support System

## Overview

This project implements a **Generative AI powered Multi-Agent System** that enables natural language interaction with both structured and unstructured data.

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
```text
Customer-Service-ChatBot/
│
├── agents/
│   ├── __init__.py
│   ├── router_bot.py          # LangGraph router (decides SQL vs RAG)
│   ├── sql_agent.py           # Handles structured SQL queries
│   └── pdf_ingest.py          # Handles PDF retrieval (Vector DB)
│
├── mcp_server/
│   ├── __init__.py
│   └── server.py              # MCP server exposing `chat()` tool
│
├── data/
│   ├── policy_docs/           # Company policy PDFs
│
├── db/             
│  ├── customer_support.db     # SQL database (structured data)
   ├── chroma_policies         # Vector DB
   ├── check_db.py             # check structured database 
   ├── init_db.py              # structured database creation
   └── seed_db.py              # sql data input
│  
├── app.py                     # Streamlit frontend UI
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── .env                       # Environment variables (API keys)
```

## Installation
### Clone the Repository
```Bash
git clone <your-repository-url>
cd Customer-Service-ChatBot
```
### Create a Virtual Environment
- macOS / Linux
```Bash
python3 -m venv venv
source venv/bin/activate
```
- Windows
```Bash
python -m venv venv
venv\Scripts\activate
```
### Install Dependencies
```Bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Configure Environment Variables
Create a .env file in the project root:
```Bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application
### Start MCP Server
```bash
uvicorn mcp_server.server:app --host 127.0.0.1 --port 8000
```

### Start Streamlit UI
```bash
streamlit run app.py
```

### Open URL
http://localhost:8501

## Demo
video URL: https://www.loom.com/share/8c81d7e893aa44b2bea83a3bfa621d31 

## Future Improvements

- Authentication & role-based access control
- Persistent memory
- Logging & monitoring
- Cloud deployment (AWS / GCP / Azure)
- Multi-user session management