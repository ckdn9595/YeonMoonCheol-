import streamlit as st


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
            st.session_state.step = 3
            
def display_page2():
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
