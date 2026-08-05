import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(page_title="Story Chatbot")

st.title("📖 AI Story Generator")

topic = st.text_input(
    "Enter a story topic:",
    placeholder="A brave dragon"
)

story_length = st.selectbox(
    "Story Length",
    ["Short", "Medium", "Long"]
)

if st.button("Generate Story"):

    if topic:

        prompt = f"""
You are a creative storyteller.

Write a {story_length.lower()} story about:

{topic}

Requirements:
- Give the story a title.
- Make it engaging.
- Use simple English.
- Include a beginning, middle, and ending.
- Keep it family-friendly.
"""

        with st.spinner("Generating Story..."):

            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                temperature=0.9,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            story = response.choices[0].message.content

        st.subheader("Generated Story")
        st.write(story)

    else:
        st.warning("Please enter a topic.")