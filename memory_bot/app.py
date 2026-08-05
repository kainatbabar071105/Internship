import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(page_title="Memory Chatbot")

st.title("...AI Memory Chatbot...")

if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#user input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Generating response..."):
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            temperature=0.9,
            messages=st.session_state.messages
        )

        assistant_response = response.choices[0].message.content

        st.session_state.history.append({"role": "assistant", "content": assistant_response})
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        with st.chat_message("assistant"):
            st.markdown(assistant_response)

            