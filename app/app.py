import sys
from pathlib import Path

# Always add project root (Customer-Chatbot) so "agents" imports work
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from agents.router_bot import answer

st.set_page_config(page_title="Customer Support Chatbot", page_icon="💬")

st.title("💬 Customer Support Chatbot")
st.caption("Ask question only related to customer and company policies.")

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
            bot_ans = answer(user_q)
        st.markdown(bot_ans)

    st.session_state.messages.append({"role": "assistant", "content": bot_ans})