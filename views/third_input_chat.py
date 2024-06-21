import streamlit as st
import re
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
def ui_reset_button():
    col1, col2, col3 = st.columns([8, 2, 3])
    with col3:
        if st.button('🗑️ 대화 내용 초기화'):
            st.session_state.inputs = [{"text": "", "type": ""}]
            st.session_state.conversations = []
            st.session_state.step = 1
            st.session_state.person1 = ""
            st.session_state.person2 = ""


def extract_name(chat_message):
    name_part = chat_message.split(':')[0]
    name = name_part.split('채팅')[-1].strip()
    return name


def remove_pattern(text):
    pattern = r'\d+번째 채팅\s+\S+\s+:'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def ui_verify_button():
    # 버튼 생성
    if st.button('검증 하기'):
        print(st.session_state.conversations)
        with st.spinner("사건 정리중.."):
            st.session_state.summary_data = summary_prompting(
                st.session_state.conversations)
            st.session_state.step = 4


def summary_prompting(data):
    data_string = ", ".join(data)
    ## open api 사용 시 주석 풀기
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": f"{data_string}",
    #         },
    #         {
    #             "role": "system",
    #             "content": """
    #                 입력된 데이터는 ([순서]번째 채팅 [주체] : [주체가 전송한 문자내용]) 형식이야.
    #                 대화에는 두 명의 주체가 있는데, 이 둘은 커플이야.
    #                 위 커플의 대화를 읽고, 잘못한 상황들을 예시와 같이 객관적으로!! 요약해줘.
    #                 중요: 각 요약이 문장의 글자 수가 30글자를 넘기지 말 것.
    #                 예시: "여자가 남자의 휴대폰을 마음대로 가져가서 검사했습니다.
    #                 """,
    #         }
    #     ],
    #     model="gpt-4o",
    # )
    # result = chat_completion.choices[0].message.content
    result = "예시용 문자 데이터"
    return result

def display_page3():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    input_field = st.session_state.inputs[0]
    with st.form(key='input_form'):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            input_field["type"] = st.radio(
                "사람 선택", [st.session_state.person1, st.session_state.person2], key="type")
            input_field["text"] = st.text_input("대화 입력", key="text")
            col1, col2, col3 = st.columns([2.125, 4, 1])
            with col2:
                submitted = st.form_submit_button(label='대화 추가하기')
            if submitted:
                if input_field["text"]:
                    idx = len(st.session_state.conversations) + 1
                    st.session_state.conversations.append(
                        f"{idx}번째 채팅 {input_field['type']} : {input_field['text']}")
                    st.session_state.inputs[0] = {"text": "", "type": ""}
                    st.experimental_rerun()
                else:
                    st.warning("입력된 대화가 없습니다. 대화를 입력해주세요.")

    ui_reset_button()
    if st.session_state.conversations:
        conversation_html = '<div class="conversation-container">'
        for idx, conversation in enumerate(st.session_state.conversations, start=1):
            clean_conversation = remove_pattern(conversation)
            name = extract_name(conversation)
            person_class = "person1" if st.session_state.person1 in conversation else "person2"
            conversation_html += f'<div class="profile{person_class}">{name}</div>'
            conversation_html += f'<div class="fixed-width-auto-height {person_class}">{clean_conversation}</div>'
        conversation_html += '</div>'
        st.markdown(conversation_html, unsafe_allow_html=True)
    else:
        st.warning("입력값이 없습니다")

    ui_verify_button()
