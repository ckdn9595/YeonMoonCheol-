import os
from openai import OpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


st.title('시나리오 봇')

keyword = st.text_input("키워드 입력")

if (st.button('생성하기')):
    with st.spinner("생성중입니다.."):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{keyword}",
                },
                {
                    "role": "system",
                    "content": "입력 받은 문장을 일본어로 번역해줘",
                }
            ],
            model="gpt-4o",
        )
    
    result = chat_completion.choices[0].message.content
    st.write(result)
