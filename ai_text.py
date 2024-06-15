import os
from openai import OpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "좋은 아침입니다.",
        },
        {
            "role": "system",
            "content": "입력 받은 문장을 일본어로 번역해줘",
        }
    ],
    model="gpt-4o",
)
result = chat_completion.choices[0].message.content
print(result)
