import streamlit as st
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_URL =  "http://127.0.0.1:8000/mcp"

async def call_mcp(question: str):
    async with streamable_http_client(MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("chat", {"question": question})

            texts = []
            for content in result.content:
                if hasattr(content, "text"):
                    texts.append(content.text)

            return "\n".join(texts)

def ask_backend(question: str):
    return asyncio.run(call_mcp(question))

st.set_page_config(page_title="Customer Support Chatbot", page_icon="💬")

st.title("💬 Customer Support Chatbot")
st.caption("Ask questions about customers and company policies.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

user_q = st.chat_input("Ask a question...")

if user_q:
    st.session_state.messages.append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            bot_ans = ask_backend(user_q)
        st.markdown(bot_ans)

    st.session_state.messages.append({"role": "assistant", "content": bot_ans})