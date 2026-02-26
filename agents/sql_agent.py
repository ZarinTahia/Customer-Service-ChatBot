from dotenv import load_dotenv
load_dotenv()

import os
import re
import sqlite3
from pathlib import Path
from typing import List, Tuple

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase

DB_PATH = Path("db/customer_support.db")

# DB schema helper
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

# Groq chat model

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4,
    max_tokens=256,
)


sql_prompt = ChatPromptTemplate.from_template("""
You are an expert at converting English questions to SQL for a SQLite database.

Use ONLY the tables/columns from this schema:
{schema}

Rules:
- Output ONLY ONE valid SQLite SELECT query.
- No markdown, no explanations, no comments, no backticks.
- Do NOT write the word "SQL".
- If the question asks for a count, use COUNT(*).
- If the question asks for a specific customer by name, match on customers.name.

Question: {question}
""")


answer_prompt = ChatPromptTemplate.from_template("""
You are a helpful customer support assistant.

Answer the user's question using ONLY the query results below.
- Do NOT show SQL.
- If results are empty, say you couldn't find it in the database.
- Be concise (1–4 sentences).

Question: {question}

Columns: {columns}
Rows: {rows}
""")

def extract_first_select(text: str) -> str:
    """Extract a SELECT statement from model output, and reject extra text."""
    m = re.search(r"(SELECT[\s\S]*?;)", text, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"(SELECT[\s\S]*)", text, flags=re.IGNORECASE)
    if m2:
        return m2.group(1).strip()
    raise ValueError(f"Model did not return a SELECT query. Got: {text}")

def run_sql(query: str) -> Tuple[List[str], List[Tuple]]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [d[0] for d in cur.description] if cur.description else []
    conn.close()
    return columns, rows

def answer_question(question: str) -> str:
    schema = db.get_table_info()

    # A) Generate SQL (ONLY)
    sql_msg = llm.invoke(sql_prompt.format_messages(schema=schema, question=question))
    sql_text = extract_first_select(sql_msg.content)

    # B) Execute
    columns, rows = run_sql(sql_text)

    # C) Turn results into English (NO SQL)
    ans_msg = llm.invoke(answer_prompt.format_messages(
        question=question,
        columns=columns,
        rows=rows
    ))
    return ans_msg.content.strip()

if __name__ == "__main__":
    q = "Which city Zarin Tahia lives?"
    print(answer_question(q))