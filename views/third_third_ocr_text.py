import streamlit as st
from PIL import Image
import os
import re
import json
from openai import OpenAI
from views.third_input_chat import ui_verify_button_separate
from views.third_input_chat import ui_verify_button_together
from views.third_input_chat import summary_prompting

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def extract_name(chat_message):
    name_part = chat_message.split(':')[0]
    name = name_part.split('채팅')[-1].strip()
    return name


def remove_pattern(text):
    pattern = r'\d+번째 채팅\s+\S+\s+:'
    if isinstance(text, list):
        text = ' '.join(text)
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def ocr_prompting():
    # OpenAI API 호출
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "user",
                "content": 
                    [
                    {"type": "text", 
                        "text": 
                        f"""
                        텍스트 형시은 대화체 한글 텍스트, 이모티콘, 줄바꿈, 다양한 글자 크기 및 서체가 포함되어있어
                        그리고 대화에는 두 명의 주체가 있는데, 이 둘은 커플이야.
                        이미지 데이터를 ([순서]번째 채팅 [주체] : [주체가 전송한 문자내용]) 형식으로 변환해줘.
                        예시: (1번째 채팅 김여자 : "너가 먼저 늦었잖아")
                        화면 기준 오른쪽 대화창은 {st.session_state.send_person}를 주체로 해주고,
                        화면 기준 왼쪽 대화창은 {st.session_state.receive_person}를 주체로 해줘
                        추가로 데이터 결과는 아래 예시와 같이 보내줘
                        1번째 채팅 김여자 : 너가 먼저 늦었잖아
                        ...
                        """
                        }
                    ] + 
                    [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}} for base64_image in st.session_state.ocr_input]
            }
        ]
    )
    result = chat_completion.choices[0].message.content
    result = result.strip().split('\n')
    for msg in result:
        st.session_state.conversations.append(msg)
    if "" in st.session_state.conversations:
        st.session_state.conversations = [item for item in st.session_state.conversations if item]
        
    return result



def display_page3_3():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    if st.session_state.ocr_input:
        ocr_prompting()
        #세션 상태 출력
        st.write("현재 세션 상태:")
        st.json(st.session_state)
        
        #채팅 출력
        with st.container(height=500, border=True):
            for idx, conversation in enumerate(st.session_state.conversations, start=1):
                if isinstance(conversation, list):
                    conversation = ' '.join(conversation)
                clean_conversation = remove_pattern(conversation)
                name = extract_name(conversation)
                person_class = "person1" if st.session_state.person1 in conversation else "person2"
                cols = st.columns([1, 8, 1])
                with cols[0]:
                    if st.session_state.get('edit_mode', False):
                        selected = st.checkbox("", key=f"checkbox_{idx}")
                        if selected:
                            st.session_state.selected_conversations.append(idx)
                        else:
                            if idx in st.session_state.selected_conversations:
                                st.session_state.selected_conversations.remove(idx)
                with cols[1]:
                    st.markdown(
                        f'''
                            <div class="{person_class}_container">
                                    <div class="profile{person_class}">{name}</div>
                                    <div class="fixed-width-auto-height {person_class}">{clean_conversation}</div>
                            </div>
                        ''',
                        unsafe_allow_html=True
                    )
    else:
        st.warning("입력값이 없습니다")

    # 작은 부제목을 표시합니다.
        st.markdown('<div class="small-subheader">연인과 같이 계신가요?</div>',
            unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        with col2:
            ui_verify_button_together()
        with col3:
            ui_verify_button_separate()
