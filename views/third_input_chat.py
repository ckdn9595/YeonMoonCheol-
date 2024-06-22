import streamlit as st
import re
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

if 'conversations' not in st.session_state:
    st.session_state.conversations = []
if 'selected_conversations' not in st.session_state:
    st.session_state.selected_conversations = []


def ui_edit_button():
    col1, col2, col3 = st.columns([8, 2, 3])
    with col3:
        if st.session_state.get('edit_mode', False):
            if st.button('편집 취소'):
                st.session_state.edit_mode = not st.session_state.get(
                    'edit_mode', False)
                st.session_state.selected_conversations = []
                st.rerun()
        else:
            if st.button('🗑️ 대화 내용 편집'):
                st.session_state.edit_mode = not st.session_state.get(
                    'edit_mode', False)
                st.rerun()


def extract_name(chat_message):
    name_part = chat_message.split(':')[0]
    name = name_part.split('채팅')[-1].strip()
    return name


def remove_pattern(text):
    pattern = r'\d+번째 채팅\s+\S+\s+:'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def ui_verify_button_separate():
    if st.button('아니요 따로 있어요.'):
        with st.spinner("사건 정리중.."):
            st.session_state.summary_data = summary_prompting(
                st.session_state.conversations)
            st.session_state.step = 4.2
            st.rerun()


def ui_verify_button_together():
    if st.button('네 같이 있어요.'):
        with st.spinner("사건 정리중.."):
            st.session_state.summary_data = summary_prompting(
                st.session_state.conversations)
            st.session_state.step = 4
            st.rerun()

def summary_prompting(data):
    data_string = ", ".join(data)
    # open api 사용 시 주석 풀기
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


def handle_delete_selected():
    st.session_state.conversations = [
        conv for idx, conv in enumerate(st.session_state.conversations, start=1)
        if idx not in st.session_state.selected_conversations
    ]
    st.session_state.selected_conversations = []
    st.session_state.edit_mode = not st.session_state.get('edit_mode', False)
    st.rerun()


def clear_text1():
    if st.session_state["text"]:
        idx = len(st.session_state.conversations) + 1
        st.session_state.conversations.append(
            f"{idx}번째 채팅 {st.session_state.person1} : {st.session_state['text']}")
        st.session_state["text"] = ""
    else:
        st.toast("입력된 대화가 없습니다. 대화를 입력해주세요.", icon="🚨")
        # st.warning("입력된 대화가 없습니다. 대화를 입력해주세요.")


def clear_text2():
    if st.session_state["text"]:
        idx = len(st.session_state.conversations) + 1
        st.session_state.conversations.append(
            f"{idx}번째 채팅 {st.session_state.person2} : {st.session_state['text']}")
        st.session_state["text"] = ""
    else:
        st.toast("입력된 대화가 없습니다. 대화를 입력해주세요.", icon="🚨")


def display_page3():
    with open("./assets/logo.svg", "r") as f:
        svg_content = f.read()

    st.markdown(
        f'<div style="padding: 1em; margin-left: 10%; margin-bottom:5%;" align="center">{svg_content}</div>', unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    with st.form(key='input_form'):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # input_field["type"] = st.radio(
            #     "사람 선택", [st.session_state.person1, st.session_state.person2], key="type")
            input_field_value = st.text_input("대화 입력", key="text")
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            with col2:
                st.form_submit_button(
                    label=st.session_state.person1, on_click=clear_text1)

            with col3:
                st.form_submit_button(
                    label=st.session_state.person2, on_click=clear_text2)

    ui_edit_button()
    if st.session_state.conversations:
        with st.container(height=500, border=True):
            for idx, conversation in enumerate(st.session_state.conversations, start=1):
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
                                st.session_state.selected_conversations.remove(
                                    idx)
                with cols[1]:

                    st.markdown(

                        f'''
                            <div class="{person_class}_container">
                                <div>
                                    <div class="profile{person_class}">{name}</div>
                                    <div class="fixed-width-auto-height {person_class}">{clean_conversation}</div>
                                </div>
                            </div>
                        ''',
                        unsafe_allow_html=True
                    )
        if st.session_state.get('edit_mode', False) and st.session_state.selected_conversations:
            if st.button("선택한 대화 삭제"):
                handle_delete_selected()

    else:
        st.warning("입력값이 없습니다")

    if not st.session_state.get('edit_mode', False) and st.session_state.conversations:
        # 작은 부제목을 표시합니다.
        st.markdown('<div class="small-subheader">연인과 같이 계신가요?</div>',
            unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        with col2:
            ui_verify_button_together()
        with col3:
            ui_verify_button_separate()
